const express = require("express");
const puppeteer = require("puppeteer");
const app = express();
require("dotenv").config();

app.get("/", async (req, res) => {
  const name = req.query.name; // name to scrape for
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto("https://google.com/?q=" + name);
  await page.screenshot({ path: "example.png" });
  res.send("Hello World!");
});

app.listen(3000, () => console.log("Example app listening on port 3000!"));
