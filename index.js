const express = require("express");
const puppeteer = require("puppeteer");
const app = express();
require("dotenv").config();

/*
TO-DO: 
  - edge cases: 
    - yourself
    - teachers
    - people who are not the first result from search
  - parse the table
  - error handling
*/

app.get("/", async (req, res) => {
  const name = req.query.name; // name to scrape for
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  console.log(name);

  //go to moongate
  await page.goto("https://moongate.cis.edu.hk");

  //login
  await page.type(
    "input#ctl00_cph_pagecontent_Login1_UserName",
    process.env.MOONGATE_USERNAME,
    { delay: 100 }
  );
  await page.type(
    "input#ctl00_cph_pagecontent_Login1_Password",
    process.env.MOONGATE_PASSWORD,
    { delay: 100 }
  );
  await page.click("input#ctl00_cph_pagecontent_Login1_LoginButton");
  await page.waitForNavigation();

  //search for the name
  await page.type("input#kw", name, { delay: 100 });
  await page.click("input#search-btn");
  await page.waitForNavigation();
  //person we want may not be the first result

  //click on results - students or results - faculty/staff
  page.click("div.views_horisontal ul li:nth-child(3) a");
  await page.waitForNavigation();

  //navigate to their profile
  page.click("table.weblist tr:first-child a");
  await page.waitFor(1000);

  //navigate to their timetable
  page.click("div#tabspagespanel ul:nth-child(3) a");
  await page.waitForNavigation();

  //grab the table (doesn't work if you do your own timetable)
  await page.waitFor(
    "#divsection_578FB9CE-05B6-4405-BCEE-07E689546B68 > div > table"
  );

  //need to use native js functions here because the ones provided in puppeteer don't seem to work
  const tableHTML = await page.evaluate(sel => {
    let table = document.querySelector(
      "#divsection_578FB9CE-05B6-4405-BCEE-07E689546B68 > div > table"
    );
    return table ? table.outerHTML : null;
  });
  console.log("test");
  res.send(tableHTML);
});

app.listen(3000, () => console.log("Example app listening on port 3000!"));
