import psycopg2
import random
import datetime
from faker import Faker
from tqdm import tqdm
from decimal import Decimal

# TO - DO :
# - FIX CONNECTION, USE EXTERNAL IP INSTEAD OF PORT-FORWARD
# - TIDDY UP CODE
# - PARALLIZE LOGS FUNC

# Configuration
DEFAULT_HOST = "localhost"  # Use localhost for port-forwarding
DEFAULT_PORT = 5432        # Standard PostgreSQL port
DEFAULT_DB = "datamart"
DEFAULT_USER = "spark"
DEFAULT_PASSWORD = "spark"

# Record counts
DEFAULT_CUSTOMERS = 2000
DEFAULT_PRODUCTS = 700
DEFAULT_ORDERS = 5000
DEFAULT_ORDER_ITEMS = 10000
DEFAULT_CONNECTION_LOGS = 50000

def get_max_id(conn, table, id_column):
    """Get the maximum ID value from a table"""
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"SELECT COALESCE(MAX({id_column}), 0) FROM {table}")
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting max ID from {table}: {e}")
            return 0

def get_table_columns(conn, table):
    """Get column names for a table"""
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_schema = 'raw' AND table_name = '{table.split('.')[1]}'
                ORDER BY ordinal_position
            """)
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting columns for {table}: {e}")
            return []

def generate_customers(conn, count):
    """Generate customer records"""
    fake = Faker()
    successful = 0
    
    # Get the highest existing id
    next_id = get_max_id(conn, "raw.customers", "customer_id") + 1
    
    # Generate and insert customers
    rows = []
    for _ in tqdm(range(count), desc="Generating customers"):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
        rows.append((next_id, first_name, last_name, email))
        next_id += 1
    
    # Insert data
    with conn.cursor() as cursor:
        for row in tqdm(rows, desc="Inserting customers"):
            try:
                cursor.execute(
                    "INSERT INTO raw.customers (customer_id, first_name, last_name, email) "
                    "VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    row
                )
                conn.commit()
                successful += 1
            except Exception as e:
                conn.rollback()
                print(f"Error inserting customer: {e}")
    
    # Report results
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM raw.customers")
        total = cursor.fetchone()[0]
        print(f"Inserted {successful} customers. Total in database: {total}")

def generate_products(conn, count):
    """Generate product records"""
    fake = Faker()
    successful = 0
    
    # Product categories for more realistic data
    categories = ["Electronics", "Clothing", "Books", "Home", "Sports", "Food", "Beauty"]
    
    # Get the highest existing id
    next_id = get_max_id(conn, "raw.products", "product_id") + 1
    
    # Generate products
    rows = []
    for _ in tqdm(range(count), desc="Generating products"):
        category = random.choice(categories)
        name = f"{category} - {fake.word().capitalize()} {fake.word().capitalize()}"
        description = fake.paragraph(nb_sentences=3)
        price = Decimal(str(round(random.uniform(9.99, 499.99), 2)))
        rows.append((next_id, name, description, price))
        next_id += 1
    
    # Insert data
    with conn.cursor() as cursor:
        for row in tqdm(rows, desc="Inserting products"):
            try:
                cursor.execute(
                    "INSERT INTO raw.products (product_id, name, description, price) "
                    "VALUES (%s, %s, %s, %s)",
                    row
                )
                conn.commit()
                successful += 1
            except Exception as e:
                conn.rollback()
                print(f"Error inserting product: {e}")
    
    # Report results
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM raw.products")
        total = cursor.fetchone()[0]
        print(f"Inserted {successful} products. Total in database: {total}")

def generate_orders(conn, count):
    """Generate order records"""
    fake = Faker()
    successful = 0
    
    # Get customer IDs from database
    with conn.cursor() as cursor:
        cursor.execute("SELECT customer_id FROM raw.customers")
        customer_ids = [row[0] for row in cursor.fetchall()]
    
    if not customer_ids:
        print("No customers found. Please generate customers first.")
        return
    
    # Get the highest existing id
    next_id = get_max_id(conn, "raw.orders", "order_id") + 1
    
    # Order statuses
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    
    # Date range (last 2 years)
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=730)
    
    # Generate orders
    rows = []
    for _ in tqdm(range(count), desc="Generating orders"):
        customer_id = random.choice(customer_ids)
        order_date = fake.date_time_between(start_date=start_date, end_date=end_date)
        status = random.choice(statuses)
        rows.append((next_id, customer_id, order_date, status))
        next_id += 1
    
    # Insert data
    with conn.cursor() as cursor:
        for row in tqdm(rows, desc="Inserting orders"):
            try:
                cursor.execute(
                    "INSERT INTO raw.orders (order_id, customer_id, order_date, status) "
                    "VALUES (%s, %s, %s, %s)",
                    row
                )
                conn.commit()
                successful += 1
            except Exception as e:
                conn.rollback()
                print(f"Error inserting order: {e}")
    
    # Report results
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM raw.orders")
        total = cursor.fetchone()[0]
        print(f"Inserted {successful} orders. Total in database: {total}")

def generate_order_items(conn, count):
    """Generate order item records"""
    successful = 0
    
    # Get order_items table columns to identify primary key column
    order_items_columns = get_table_columns(conn, "raw.order_items")
    if not order_items_columns:
        print("Could not determine order_items table structure.")
        return
    
    # The first column is usually the primary key
    primary_key_column = order_items_columns[0]
    print(f"Using '{primary_key_column}' as the primary key for order_items table.")
    
    # Get order IDs from database
    with conn.cursor() as cursor:
        cursor.execute("SELECT order_id FROM raw.orders")
        order_ids = [row[0] for row in cursor.fetchall()]
    
    if not order_ids:
        print("No orders found. Please generate orders first.")
        return
    
    # Get product IDs and prices from database
    with conn.cursor() as cursor:
        cursor.execute("SELECT product_id, price FROM raw.products")
        products = cursor.fetchall()
    
    if not products:
        print("No products found. Please generate products first.")
        return
    
    # Get the highest existing id
    next_id = get_max_id(conn, "raw.order_items", primary_key_column) + 1
    
    # Generate order items
    rows = []
    for _ in tqdm(range(count), desc="Generating order items"):
        order_id = random.choice(order_ids)
        product_id, price = random.choice(products)
        quantity = random.randint(1, 5)
        
        # Convert to Decimal for calculation
        price_decimal = price if isinstance(price, Decimal) else Decimal(str(price))
        adjusted_price = price_decimal * Decimal(str(random.uniform(0.95, 1.05)))
        adjusted_price = adjusted_price.quantize(Decimal('0.01'))
        
        rows.append((next_id, order_id, product_id, quantity, adjusted_price))
        next_id += 1
    
    # Insert data
    with conn.cursor() as cursor:
        # Determine correct column names based on table structure
        columns = [primary_key_column, "order_id", "product_id", "quantity", "price"]
        columns_sql = ", ".join(columns)
        
        for row in tqdm(rows, desc="Inserting order items"):
            try:
                cursor.execute(
                    f"INSERT INTO raw.order_items ({columns_sql}) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    row
                )
                conn.commit()
                successful += 1
            except Exception as e:
                conn.rollback()
                print(f"Error inserting order item: {e}")
    
    # Report results
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM raw.order_items")
        total = cursor.fetchone()[0]
        print(f"Inserted {successful} order items. Total in database: {total}")

def generate_connection_logs(conn, count):
    """Generate connection log records with skewed distribution"""
    fake = Faker()
    successful = 0
    chunk_size = 1000  # Process in chunks for progress reporting
    
    # Get connection_logs table columns to identify primary key column
    logs_columns = get_table_columns(conn, "raw.connection_logs")
    if not logs_columns:
        print("Could not determine connection_logs table structure.")
        return
    
    # The first column is usually the primary key
    primary_key_column = logs_columns[0]
    print(f"Using '{primary_key_column}' as the primary key for connection_logs table.")
    
    # Countries with skewed distribution
    countries = ["US", "UK", "DE", "FR", "CN", "IN", "BR", "JP", "CA", "AU"]
    country_weights = [0.4, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.03, 0.02]
    
    # User IDs
    user_ids = [f"user_{i:03d}" for i in range(1, 501)]
    
    # Statuses with distribution
    statuses = ["success", "failed_password", "failed_network", "timeout", "rate_limited"]
    status_weights = [0.85, 0.06, 0.04, 0.03, 0.02]
    
    # Date range (last 3 months)
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=90)
    
    # Get the highest existing id
    next_id = get_max_id(conn, "raw.connection_logs", primary_key_column) + 1
    
    # Process in chunks to show progress
    for chunk_start in range(0, count, chunk_size):
        chunk_end = min(chunk_start + chunk_size, count)
        chunk_size_actual = chunk_end - chunk_start
        
        # Generate chunk of logs
        rows = []
        for _ in tqdm(range(chunk_size_actual), 
                      desc=f"Generating logs {chunk_start+1}-{chunk_end} of {count}"):
            user_id = random.choice(user_ids)
            timestamp = fake.date_time_between(start_date=start_date, end_date=end_date)
            country = random.choices(countries, weights=country_weights, k=1)[0]
            ip_address = fake.ipv4()
            status = random.choices(statuses, weights=status_weights, k=1)[0]
            duration_seconds = random.randint(1, 300)
            rows.append((next_id, user_id, timestamp, country, ip_address, status, duration_seconds))
            next_id += 1
        
        # Insert chunk
        with conn.cursor() as cursor:
            # Determine correct column names based on table structure
            columns = [primary_key_column, "user_id", "timestamp", "country", 
                      "ip_address", "status", "duration_seconds"]
            columns_sql = ", ".join(columns)
            
            for row in tqdm(rows, desc=f"Inserting logs {chunk_start+1}-{chunk_end}"):
                try:
                    cursor.execute(
                        f"INSERT INTO raw.connection_logs ({columns_sql}) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        row
                    )
                    conn.commit()
                    successful += 1
                except Exception as e:
                    conn.rollback()
                    if successful % 100 == 0:  # Limit error output
                        print(f"Error inserting connection log: {e}")
        
        print(f"Inserted {successful} of {chunk_end} connection logs so far...")
    
    # Report final results
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM raw.connection_logs")
        total = cursor.fetchone()[0]
        print(f"Inserted {successful} connection logs. Total in database: {total}")

def main():
    try:
        print(f"Connecting to PostgreSQL at {DEFAULT_HOST}:{DEFAULT_PORT}...")
        with psycopg2.connect(
            host=DEFAULT_HOST,
            port=DEFAULT_PORT,
            database=DEFAULT_DB,
            user=DEFAULT_USER,
            password=DEFAULT_PASSWORD
        ) as conn:
            print("Connected successfully!")
            
            # # Generate data - each function handles its own errors
            # generate_customers(conn, DEFAULT_CUSTOMERS)
            # generate_products(conn, DEFAULT_PRODUCTS)
            # generate_orders(conn, DEFAULT_ORDERS)
            # generate_order_items(conn, DEFAULT_ORDER_ITEMS)
            generate_connection_logs(conn, DEFAULT_CONNECTION_LOGS)
            
            print("Data generation complete!")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()
