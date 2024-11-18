// import {setTimeout} from "node:timers/promises";
const puppeteer = require('puppeteer'); 
const cheerio = require('cheerio');
const fs = require('fs');
const { writeFile } = require('fs/promises');
const csvParser = require('csv-parser');

 
(async () => {
	
	const taxonIds = [];

	fs.createReadStream('species_lineage.csv')
        .pipe(csvParser())
        .on('data', (row) => {
			// console.log(row["NCBI Taxon ID"])
			// console.log(row)
            taxonIds.push({"species": row["Species"], "taxid": row["NCBI Taxon ID"]}); // Assuming the taxon ID is in the second column
        })
		.on('end', async () => {
            console.log('CSV file successfully processed.');
		

    // Launch Puppeteer
	const browser = await puppeteer.launch({
		executablePath: '/usr/bin/chromium-browser',
		headless: false
	  })
    const page = await browser.newPage();

	const results =[];

	for (const data of taxonIds){
		try {
			const url = `https://www.ncbi.nlm.nih.gov/datasets/genome/?taxon=${data["taxid"]}`
			await page.goto(url, { waitUntil: 'networkidle2' });
			const content = await page.content();
			const $ = cheerio.load(content);

			// Parse the first table (or specify a unique selector)
			const table = $('table').first();
		
			// Iterate over each row and get the cell data
			table.find('tr').each((index, element) => {
				const row = $(element).find('td').map((i, el) => $(el).text().trim()).get();
				console.log(row)
				if (row.length > 2 && row[4] == data["species"]) {
					console.log('Row:', row);
					let new_data = data

					if (row[3] != "") {
						new_data["GA"] = row[3]
					} else {
						new_data["GA"] = row[2]
					}
					results.push(new_data)
					console.log(results)
					return false;

				} else if (row.length > 2 && row[4] != data["species"]){
					let new_data = data
					new_data["GA"] = ""
					results.push(new_data)
					return false;
				}
			});
		console.log("done")
		}catch (error){
			console.error(`Error processing Taxon ID ${taxonID}:`, error);
		}
	} 
	browser.close()

	fs.writeFile("data.json", JSON.stringify(results, null, 2), (err)=>{})

    // Navigate to the website
    

    // Wait for 10 seconds if needed
    // await page.waitForTimeout(10000);

    // Get page content
    // const content = await page.content();

    // // Close the browser
    // await browser.close();

    // // Load content into Cheerio
    // const $ = cheerio.load(content);

    // // Parse the first table (or specify a unique selector)
    // const table = $('table').first();

    // // Iterate over each row and get the cell data
    // table.find('tr').each((index, element) => {
    //     const row = $(element).find('td').map((i, el) => $(el).text().trim()).get();
    //     if (row.length) {
    //         console.log('Row:', row);
    //     }
    // });})
})})();