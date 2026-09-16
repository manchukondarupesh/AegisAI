const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// Connect DB
mongoose.connect("mongodb://127.0.0.1:27017/foodDB")
.then(() => console.log("MongoDB Connected"))
.catch(err => console.log(err));

// Models
const Food = mongoose.model("Food", {
  name: String,
  price: Number,
  image: String
});

const Order = mongoose.model("Order", {
  items: Array,
  total: Number
});

// Routes

// Get foods
app.get("/foods", async (req, res) => {
  const foods = await Food.find();
  res.json(foods);
});

// Add food
app.post("/foods", async (req, res) => {
  const food = new Food(req.body);
  await food.save();
  res.json(food);
});

// Place order
app.post("/order", async (req, res) => {
  const order = new Order(req.body);
  await order.save();
  res.json({ message: "Order placed!" });
});

app.listen(5000, () => console.log("Server running on port 5000"));