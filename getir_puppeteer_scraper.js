const puppeteer = require('puppeteer');
const fs = require('fs');

async function scrapeGetir() {
    const browser = await puppeteer.launch({
        headless: "new",
        args: ['--no-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // User agent'ı ayarla
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
        
        // Getir ana sayfasına git
        await page.goto('https://getir.com/kategori/temel-gida', {
            waitUntil: 'networkidle0'
        });
        
        // Ürünleri topla
        const products = await page.evaluate(() => {
            const items = [];
            const cards = document.querySelectorAll('[data-testid="product-card"]');
            
            cards.forEach(card => {
                try {
                    const name = card.querySelector('[data-testid="product-name"]').textContent;
                    const price = card.querySelector('[data-testid="product-price"]').textContent;
                    const image = card.querySelector('img').src;
                    
                    items.push({
                        name,
                        price,
                        image
                    });
                    
                    console.log(`Ürün eklendi: ${name} - ${price}`);
                } catch (e) {
                    console.log('Ürün bilgisi alınamadı:', e);
                }
            });
            
            return items;
        });
        
        // Sonuçları kaydet
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `getir_products_${timestamp}.json`;
        
        fs.writeFileSync(filename, JSON.stringify(products, null, 4), 'utf8');
        console.log(`Veriler başarıyla ${filename} dosyasına kaydedildi.`);
        
    } catch (e) {
        console.error('Hata oluştu:', e);
    } finally {
        await browser.close();
    }
}

scrapeGetir(); 