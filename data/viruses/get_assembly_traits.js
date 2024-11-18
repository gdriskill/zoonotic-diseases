// import {setTimeout} from "node:timers/promises";
const puppeteer = require('puppeteer'); 
const cheerio = require('cheerio');
const fs = require('fs');
const { writeFile } = require('fs/promises');
const csvParser = require('csv-parser');

 
(async () => {
	
	const assemblies = [];

	fs.createReadStream('updated_species_assembly.csv')
        .pipe(csvParser())
        .on('data', (row) => {
			// console.log(row["NCBI Taxon ID"])
			// console.log(row)
            assemblies.push({"species": row["Pathogen Species"], "GA": row["GA"]});
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

	for (const assembly of assemblies){
		if (assembly["GA"].startsWith("GC")) {

			try {
				const url = `https://www.ncbi.nlm.nih.gov/datasets/genome/${assembly["GA"]}/`
				await page.goto(url, { waitUntil: 'networkidle2' });
				const content = await page.content();
				const $ = cheerio.load(content);

				const table_stats = $('[data-section="genome_statistics"] table');;
				
				let newData = assembly
				

				table_stats.find('tr').each((index, element) => {
					const row = $(element).find('td').map((i, el) => {
						let is_genome = false;
						const row_text = $(element).find('td').map((i, el) => {
							let text = $(el).text().trim()
							if (is_genome) {
								text = $(el).find("span").attr("aria-label")
								is_genome = false
							}
							if (text == "Genome size") {
								is_genome = true;
							}
							return text
						}
						).get();

						if (row_text.length > 1 && row_text[0] == "Genome size") {
							newData["size"] = row_text[1]
						}
						if (row_text.length > 1 && row_text[0] == "GC percent") {
							newData["gc"] = row_text[1]
						}
						return 
					}
					).get();
				})

				const table_annot = $('[data-section="annotation_details"] table');;

				table_annot.find('tr').each((index, element) => {
					const row = $(element).find('td').map((i, el) => {
						let is_genome = false;
						const row_text = $(element).find('td').map((i, el) => {
							let text = $(el).text().trim()
							return text
						}
						).get();

						if (row_text.length > 1 && row_text[0] == "Genes") {
							newData["genes"] = row_text[1]
						}
						return 
					}
					).get();
				})

				console.log(newData)

				results.push(newData)
	
				console.log("done")
			}catch (error){
				console.error(`Error processing Taxon ID ${assembly["species"]}:`, error);
			}
		}

	} 
	browser.close()

	fs.writeFile("genome_stats.json", JSON.stringify(results, null, 2), (err)=>{})

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