
import pandas as pd
import mysql.connector

# 1. Load Delhivery dataset
df = pd.read_csv(
    "data/delhivery_data.csv",
    encoding="utf-8"
)

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

# 2. Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Enter your MySQL password if required
    database="DelhiveryAnalytics"
)

cursor = conn.cursor()

# 3. Create table using Delhivery columns
create_table_sql = """
CREATE TABLE IF NOT EXISTS delhivery_data (
    `data` VARCHAR(30),
    `trip_creation_time` DATETIME(6),
    `route_schedule_uuid` VARCHAR(150),
    `route_type` VARCHAR(50),
    `trip_uuid` VARCHAR(100),
    `source_center` VARCHAR(50),
    `source_name` VARCHAR(200),
    `destination_center` VARCHAR(50),
    `destination_name` VARCHAR(200),
    `od_start_time` DATETIME(6),
    `od_end_time` DATETIME(6),
    `start_scan_to_end_scan` DOUBLE,
    `is_cutoff` TINYINT(1),
    `cutoff_factor` INT,
    `cutoff_timestamp` DATETIME(6),
    `actual_distance_to_destination` DOUBLE,
    `actual_time` DOUBLE,
    `osrm_time` DOUBLE,
    `osrm_distance` DOUBLE,
    `factor` DOUBLE,
    `segment_actual_time` DOUBLE,
    `segment_osrm_time` DOUBLE,
    `segment_osrm_distance` DOUBLE,
    `segment_factor` DOUBLE
)
"""

try:
    cursor.execute(create_table_sql)
    conn.commit()

    # 4. Prepare INSERT query from actual CSV columns
    columns = [f"`{col}`" for col in df.columns]
    column_names = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(df.columns))

    sql = f"""
        INSERT INTO delhivery_data ({column_names})
        VALUES ({placeholders})
    """

    # 5. Handle missing values
    df = df.astype(object).where(pd.notnull(df), None)

    # Convert Boolean values into MySQL-compatible integers
    if "is_cutoff" in df.columns:
        df["is_cutoff"] = df["is_cutoff"].map(
            lambda x: int(x) if x is not None else None
        )

    # 6. Insert records in batches
    batch_size = 5000
    total_rows = len(df)

    for start in range(0, total_rows, batch_size):
        batch = df.iloc[start:start + batch_size]

        data = [
            tuple(row)
            for row in batch.itertuples(index=False, name=None)
        ]

        cursor.executemany(sql, data)
        conn.commit()

        print(
            f"Imported {min(start + batch_size, total_rows)}"
            f" / {total_rows} rows"
        )

    print("Delhivery dataset imported successfully!")

except Exception as e:
    conn.rollback()
    print("Import error:", e)

finally:
    cursor.close()
    conn.close()
