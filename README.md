# Talk to DB 🤖💬📊 (WIP- Work in Progress)

## Overview

Talk to DB is an innovative AI-powered database query assistant that helps non-technical people extract queries from databases effortlessly. By leveraging natural language processing, users can interact with databases using plain English.

I have developed this application in an AI Hackathon within 30 minutes and later, added more features to it.

The main motiviation to develop this to make it easier for non-technical people to extract queries from databases effortlessly. Further, i see this problem in my day to day work and i think this can be a game changer for non-technical people to extract queries from databases effortlessly.

## 🌟 Key Features

- **Natural Language to SQL**: Convert everyday language into precise SQL queries
- **User-Friendly Interface**: No technical expertise required
- **Powered by OpenAI**: Advanced language understanding
- **PostgreSQL Integration**: Works seamlessly with PostgreSQL databases

## 🚀 Quick Example

### Sample Query
```json
{
  "string": "list out the film names that are connected with actor_id 4"
}
```

This query will generate and execute a SQL statement to retrieve all film names associated with actor ID 4.

## 🔍 How It Works

1. User enters a natural language query
2. AI converts the query to a SQL statement
3. Query is executed against the database
4. Results are returned in a readable format

## 💡 Use Cases

- Business Analysts
- Managers without SQL knowledge
- Students learning database interactions
- Quick data exploration

## 🛠 Technologies

- FastAPI
- OpenAI GPT
- SQLAlchemy
- PostgreSQL
- Docker

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License