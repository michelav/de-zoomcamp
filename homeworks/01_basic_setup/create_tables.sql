CREATE TABLE "yellow_taxi_data" (
"VendorID" INTEGER,
  "tpep_pickup_datetime" TIMESTAMP,
  "tpep_dropoff_datetime" TIMESTAMP,
  "passenger_count" INTEGER,
  "trip_distance" REAL,
  "RatecodeID" INTEGER,
  "store_and_fwd_flag" TEXT,
  "PULocationID" INTEGER,
  "DOLocationID" INTEGER,
  "payment_type" INTEGER,
  "fare_amount" REAL,
  "extra" REAL,
  "mta_tax" REAL,
  "tip_amount" REAL,
  "tolls_amount" REAL,
  "improvement_surcharge" REAL,
  "total_amount" REAL,
  "congestion_surcharge" REAL
);

CREATE TABLE "taxi_zone" (
"LocationID" INTEGER,
  "Borough" TEXT,
  "Zone" TEXT,
  "service_zone" TEXT
);