import pandas as pd
from jinja2 import Template
import os

# Load the sales data
df = pd.read_csv("cleaned_sales_data.csv", parse_dates=["data"])

# Save a preview for visual verification (optional)
df.head(10).to_csv("sample_preview.csv", index=False)

# Generate JSON model for pbi-tools using Jinja2 template
model_template = """
{
  "tables": [
    {
      "name": "SalesData",
      "columns": [
        { "name": "data", "dataType": "dateTime" },
        { "name": "venda", "dataType": "int64" },
        { "name": "estoque", "dataType": "int64" },
        { "name": "preco", "dataType": "double" },
        { "name": "year", "dataType": "int64" },
        { "name": "month", "dataType": "int64" },
        { "name": "day", "dataType": "int64" },
        { "name": "weekday", "dataType": "string" },
        { "name": "venda_7day_avg", "dataType": "double" },
        { "name": "category", "dataType": "string" },
        { "name": "store", "dataType": "string" },
        { "name": "region", "dataType": "string" }
      ],
      "measures": [
        { "name": "Total Sales", "expression": "SUM(SalesData[venda])" },
        { "name": "Avg Sales", "expression": "AVERAGE(SalesData[venda])" },
        { "name": "Low Stock Alerts", "expression": "COUNTROWS(FILTER(SalesData, SalesData[estoque] < 50))" }
      ]
    }
  ]
}
"""

# Write the data model JSON to disk
with open("model.json", "w") as f:
    f.write(Template(model_template).render())

print("✅ Data model generated as model.json")
print("➡️  Now run the following in terminal using pbi-tools:")
print("    pbi-tools new --project SalesDashboard --template model.json --data-source cleaned_sales_data.csv")
