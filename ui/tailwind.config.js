/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./public/index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                // Основная цветовая схема Альфа-Банка
                alpha: {
                    50: '#FFEFF0',
                    100: '#FFE0E1',
                    200: '#FFCDCF',
                    300: '#FFA7AA',
                    400: '#FF8185',
                    500: '#EF3124', // Основной красный цвет Альфа-Банка
                    600: '#CF2A1E',
                    700: '#AF2319',
                    800: '#8F1B15',
                    900: '#6F1410',
                },
                // Нейтральные цвета
                neutral: {
                    50: '#F8F9FA',
                    100: '#F1F3F5',
                    200: '#E9ECEF',
                    300: '#DEE2E6',
                    400: '#CED4DA',
                    500: '#ADB5BD',
                    600: '#6C757D',
                    700: '#495057',
                    800: '#343A40',
                    900: '#212529',
                },
            },
            // Сохраняем прежние цвета indigo для обратной совместимости, но добавляем цвета альфа
            fontFamily: {
                sans: ['"SF Pro Display"', '"Styrene A LC"', 'Inter', 'sans-serif'],
            },
        },
    },
    plugins: [],
} 