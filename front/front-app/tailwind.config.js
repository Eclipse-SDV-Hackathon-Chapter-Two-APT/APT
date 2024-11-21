/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // React 프로젝트
    "./public/index.html"         // HTML 포함
  ],
  theme: {
    extend: {}, // 커스터마이징 가능
  },
  plugins: [],
};