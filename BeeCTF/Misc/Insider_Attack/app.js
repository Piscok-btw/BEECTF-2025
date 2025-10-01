const dotenv = require('dotenv');
dotenv.config({ path: './.env' }); // pastikan path sesuai

console.log("DATABASE_URL:", process.env.DATABASE_URL);
console.log("SECRET_KEY:", process.env.SECRET_KEY);
console.log("API_KEY:", process.env.API_KEY);
console.log("DISCORD_BOT_TOKEN:", process.env.DISCORD_BOT_TOKEN);
