import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df=pd.read_csv("data/delhivery_data.csv")
# print("Dataset Shape:",df.shape)
# print("First 5 row:",df.head())
# print("Columns name:",df.columns.tolist())
# print("Data Types",df.dtypes)

# print("Missing Values",df.isnull().sum().sort_values(ascending=False))
# print("Exact Duplicate Rows",df.duplicated().sum())
# print("Total Rows",len(df))
# print("Unique Trips",df["trip_uuid"].nunique())
# print("Dataset Information:",df.info())

# print("Unique Trips:", df["trip_uuid"].nunique())
# print("Before Cleaning:")
# print("Missing Source Name",df["source_name"].isna().sum())
# print("Missing Destination Name",df["destination_name"].isna().sum())
df_clean=df.copy()
df_clean["source_name"]=df_clean["source_name"].fillna("Unknown")
df_clean["destination_name"]=df_clean["destination_name"].fillna("Unknown")
# print("After Cleaning:")
# print("Missing Source Name",df_clean["source_name"].isna().sum())
# print("Missing Destination Name",df_clean["destination_name"].isna().sum())
# print("Cleaned dataset Shape",df_clean.shape)

date_columns=[
    "trip_creation_time",
    "od_start_time",
    "od_end_time",
    "cutoff_timestamp"
]
for col in date_columns:
    df_clean[col]=pd.to_datetime(
        df_clean[col],
        errors="coerce"
    )
# print("Updaterd Date Data Types:",df_clean[date_columns].dtypes)
# print("Invalid Dates after Coneversion",df_clean[date_columns].isna().sum())
# print("\nDate range:")
# print("Start:", df_clean["trip_creation_time"].min())
# print("End:", df_clean["trip_creation_time"].max())    

trip_summary=(
    df_clean.groupby("trip_uuid",as_index=False).agg( source_name=("source_name", "first"),
        destination_name=("destination_name", "first"),
        actual_time=("actual_time", "max"),
        osrm_time=("osrm_time", "max"),
        actual_distance=("actual_distance_to_destination", "max"),
        osrm_distance=("osrm_distance", "max"))
)

trip_summary["time_difference"]=(
    trip_summary["actual_time"]-trip_summary["osrm_time"]    
)

trip_summary["time_ratio"]=(
    trip_summary["actual_time"]/trip_summary["osrm_time"].replace(0,np.nan)
    )
trip_summary["distance_difference"]=(
       trip_summary["actual_distance"] - trip_summary["osrm_distance"]
)
# print("Trip Level Shape:",trip_summary.shape)
# print("Time Difference summmary:",)
# print(trip_summary["time_difference"].describe())
# print("\nTop 10 trips by time difference:")
# print(
#     trip_summary.nlargest(10, "time_difference")[
#         [
#             "trip_uuid",
#             "source_name",
#             "destination_name",
#             "actual_time",
#             "osrm_time",
#             "time_difference",
#             "time_ratio"
#         ]
#     ]
# )

trip_legs=(df_clean.groupby("trip_uuid").agg(rows=("trip_uuid", "size"),
        unique_sources=("source_center", "nunique"),
        unique_destinations=("destination_center", "nunique"),
        unique_routes=("route_schedule_uuid", "nunique")
    )
    .reset_index())
# print("Trips with Multiple Source Centers:",(trip_legs["unique_sources"]>1).sum())
# print("Trips with Multiple destination Centers:",(trip_legs["unique_destinations"]>1).sum())
# print("Trips with Multiple destination Centers:",(trip_legs["unique_routes"]>1).sum())
# print("Example Trip With multiple route legs:")
example_trip=trip_legs.loc[
    (trip_legs["unique_sources"]>1) | (trip_legs["unique_destinations"]>1),
    "trip_uuid"
    ].head(1)
# if not example_trip.empty:
#     sample = df_clean[
#         df_clean["trip_uuid"] == example_trip.iloc[0]
#     ]

#     print(sample[
#         [
#             "trip_uuid",
#             "route_schedule_uuid",
#             "source_center",
#             "destination_center",
#             "actual_time",
#             "osrm_time",
#             "actual_distance_to_destination"
#         ]
#     ].to_string(index=False))

route_summary=(
    df_clean.groupby(
        ["trip_uuid", "route_schedule_uuid",
            "source_center",
            "destination_center"],as_index=False
    ).agg(
         source_name=("source_name", "first"),
        destination_name=("destination_name", "first"),
        actual_time=("actual_time", "max"),
        osrm_time=("osrm_time", "max"),
        actual_distance=(
            "actual_distance_to_destination", "max"
        ),
        osrm_distance=("osrm_distance", "max")
    )
)
route_summary["time_difference"]=(
    route_summary["actual_time"]-route_summary["osrm_time"]
)
route_summary["time_ratio"]=(
    route_summary["actual_time"]/route_summary["osrm_time"].replace(0,np.nan)

)
# print("Original rows:", len(df_clean))
# print("Unique trips:", df_clean["trip_uuid"].nunique())
# print("Route-level records:", len(route_summary))
# print("Time Difference Summary:",route_summary["time_difference"].describe())
# print("\nTop 10 route legs by time difference:")
# print(
#     route_summary.nlargest(10, "time_difference")[
#         [
#             "trip_uuid",
#             "source_name",
#             "destination_name",
#             "actual_time",
#             "osrm_time",
#             "time_difference",
#             "time_ratio"
#         ]
#     ].to_string(index=False)
# )


q1 = route_summary["time_difference"].quantile(0.25)
q3 = route_summary["time_difference"].quantile(0.75)

iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = route_summary[
    (route_summary["time_difference"] < lower_bound) |
    (route_summary["time_difference"] > upper_bound)
].copy()

# print("Q1:", q1)
# print("Q3:", q3)
# print("IQR:", iqr)
# print("Lower bound:", lower_bound)
# print("Upper bound:", upper_bound)

# print("\nTotal outlier records:", len(outliers))
# print(
#     "Outlier percentage:",
#     round(len(outliers) / len(route_summary) * 100, 2),
#     "%"
# )

# print("\nTop 10 outlier route legs:")
# print(
#     outliers.nlargest(10, "time_difference")[
#         [
#             "source_name",
#             "destination_name",
#             "actual_time",
#             "osrm_time",
#             "time_difference",
#             "time_ratio"
#         ]
#     ].to_string(index=False)
# )

# plt.figure(figsize=(10,5))
# plt.hist(route_summary["time_difference"].dropna(),bins=50)
# plt.axvline(upper_bound,linestyle="--",label=f"Upper outlier bound:{upper_bound}")
# plt.title("Distribution of Actual vs Estimated Time Difference")
# plt.xlabel("Time Difference (dataset units)")
# plt.ylabel("Number of Route Records")
# plt.legend()
# plt.tight_layout()
# plt.show()
# plt.figure(figsize=(8,6))
# plt.scatter(
#     route_summary["osrm_time"],route_summary["actual_time"],alpha=0.3
# )
# plt.title("Actual Time vs OSRM Estimated Time")
# plt.xlabel("OSRM Estimated Time (dataset units)")
# plt.ylabel("Actual Time (dataset units)")
# plt.tight_layout()
# plt.show()

# top10=route_summary.nlargest(10,"time_difference").copy()
# top10["route"] = (
#     top10["source_name"].str.slice(0, 18)
#     + " → "
#     + top10["destination_name"].str.slice(0, 18)
# )

# plt.figure(figsize=(12,7))
# plt.barh(top10["route"],top10["time_difference"])
# plt.gca().invert_yaxis()
# plt.title("Top 10 Route Records by Time Difference")
# plt.xlabel("Time Difference (dataset units)")
# plt.tight_layout()
# plt.show()


total_routes = len(route_summary)

avg_difference = route_summary["time_difference"].mean()
median_difference = route_summary["time_difference"].median()

above_estimate = (
    route_summary["time_difference"] > 0
).sum()

below_estimate = (
    route_summary["time_difference"] < 0
).sum()

equal_estimate = (
    route_summary["time_difference"] == 0
).sum()

# print("\n========== BUSINESS INSIGHTS ==========")

# print("Total route records:", total_routes)

# print(
#     "Average actual vs estimated time difference:",
#     round(avg_difference, 2)
# )

# print(
#     "Median actual vs estimated time difference:",
#     round(median_difference, 2)
# )

# print(
#     "Routes where actual time was higher:",
#     above_estimate
# )

# print(
#     "Routes where actual time was lower:",
#     below_estimate
# )

# print(
#     "Routes where actual time equalled estimate:",
#     equal_estimate
# )

# print(
#     "Potential outlier records:",
#     len(outliers)
# )

# print(
#     "Potential outlier percentage:",
#     round(len(outliers) / total_routes * 100, 2),
#     "%"
# )

# Save cleaned dataset for Power BI
# Export route-level summary for Power BI
import os

output_path = "data/delhivery_route_summary.csv"
os.makedirs("data", exist_ok=True)

route_summary.to_csv(output_path, index=False)

print("Route summary exported successfully!")
print("Rows:", len(route_summary))
print("Columns:", len(route_summary.columns))
print("File:", os.path.abspath(output_path))