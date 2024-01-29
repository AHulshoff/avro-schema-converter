from icecream import ic
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, BooleanType, IntegerType, ArrayType, TimestampType
from fastavro import writer, reader, schema
from avro.schema import parse
from avro.io import DatumWriter, DatumReader
from avro.datafile import DataFileWriter, DataFileReader
import json
from json_to_avro_schema import Converter

with open("test.json") as f:
    json_data = json.load(f)
    avro_schema = Converter("weatherforecast", json.dumps(json_data)).avro_schema
    writer = DataFileWriter(open("test.avro", "wb"), DatumWriter(), avro_schema)
    writer.append(json_data)
    writer.close()


    reader = DataFileReader(open("test.avro", "rb"), DatumReader())
    ic(reader.schema)
    reader.close()