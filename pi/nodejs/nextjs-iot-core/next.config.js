const withPWA = require('next-pwa')

module.exports = withPWA({
  env: {
    serverUrl: "127.0.0.1:81",
  },
  pwa: {
    dest: "public",
    disable: process.env.NODE_ENV === "development",
  },
});