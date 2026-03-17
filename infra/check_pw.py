from passlib.context import CryptContext
ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
h = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4NwKXkLQPHHKq0Ky"
print("password123 matches:", ctx.verify("password123", h))
print("New hash for password123:", ctx.hash("password123"))
