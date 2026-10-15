// Step 2: switch to the bookstore database
// use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list authors and books
printjson(db.authors.find().toArray())
printjson(db.books.find().toArray())

// Step 6: insert two new books
db.books.insertMany([
  { title: "The Hobbit", published_year: 1937, author_ids: ["author_004"] },
  { title: "Coraline", published_year: 2002, author_ids: ["author_002"] }
])

// Step 7: add missing authors
db.authors.insertOne({
  _id: "author_004",
  name: "J.R.R. Tolkien",
  nationality: "British",
  bio: {
    short: "English writer and philologist, author of The Hobbit and The Lord of the Rings.",
    long: "J.R.R. Tolkien was an English writer and Oxford professor of language and literature. He is best known for The Hobbit and The Lord of the Rings, which shaped modern fantasy through invented languages, deep histories, and the world of Middle-earth."
  }
})

// Step 8: filter books by a list of authors (one loaded, one added)
printjson(db.books.find({ author_ids: { $in: ["author_002", "author_004"] } }).toArray())