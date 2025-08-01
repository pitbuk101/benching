# API BRIDGE

This code is bridge between Text2SQL AI Bot and SoureAI Bot

## API Payload Contract

```json
{
    "query": "Question Related to the bot"
}

```

## API Response Contract

### Success Response

```json
{
    "original_query" : "Orginal Question Asked",
    "result": {
        "data": {
            "previewData": {
                "correlationId":"e38009ab-8ca6-4052-84bb-223ce2a6f2f0",
                "columns": [
                    {
                        "name": "TotalSpends",
                        "type": "float64"
                    }
                ],
                "data": [
                    [
                        4644401710.939392
                    ]
                ]
            }
        }
  },
    "count": 1,
    "status_code": 200,
    "sql": "Select TotalSpends from spends_table",
    "thread_id": 1234
}
```

### Error Response

```json
{
    "error": "No data Found",
    "status_code": 200
}

```
