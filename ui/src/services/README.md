# Сервисы UI приложения финансовой грамотности

Этот каталог содержит все сервисы для взаимодействия с backend API и управления состоянием приложения.

## Обзор сервисов

### 🔧 ApiService
Базовый сервис для HTTP запросов к backend API.

**Основные возможности:**
- Управление токенами авторизации
- Реальные HTTP запросы к backend API
- Обработка ошибок и автоматический logout при 401
- Логирование всех запросов

**Использование:**
```javascript
import ApiService from '@/services/ApiService';

// GET запрос
const data = await ApiService.get('/users/profile');

// POST запрос
const result = await ApiService.post('/lessons/1/start', { data });
```

### 🔐 AuthService
Сервис авторизации и управления пользователями.

**Основные возможности:**
- Регистрация и авторизация пользователей
- Управление JWT токенами
- Обновление профиля пользователя
- Смена и восстановление пароля
- Автоматическое сохранение в localStorage

**Использование:**
```javascript
import AuthService from '@/services/AuthService';

// Авторизация
const result = await AuthService.login({ email, password });

// Получение текущего пользователя
const user = AuthService.getUser();

// Проверка авторизации
const isLoggedIn = AuthService.isLoggedIn();
```

### 📚 LessonService
Сервис для работы с уроками и обучением.

**Основные возможности:**
- Получение уроков и их контента с backend
- Отслеживание прогресса обучения
- Работа с тестами и квизами
- AI валидация ответов
- Начисление коинов за прогресс
- Рекомендации уроков

**Использование:**
```javascript
import { LessonService } from '@/services/LessonService';

// Получение урока
const lesson = await LessonService.getLesson(1);

// Начало урока
await LessonService.startLesson(1);

// Отправка ответа на тест
const result = await LessonService.submitQuizAnswer(quizId, answer);
```

### 🎮 GamificationService
Сервис геймификации с коинами, челленджами и достижениями.

**Основные возможности:**
- Управление коинами пользователя
- Челленджи и их прогресс
- Массовые события
- Таблица лидеров
- История транзакций
- Статистика геймификации

**Использование:**
```javascript
import GamificationService from '@/services/GamificationService';

// Получение баланса коинов
const coins = await GamificationService.getUserCoins();

// Присоединение к челленджу
await GamificationService.joinChallenge(challengeId);

// Получение лидерборда
const leaderboard = await GamificationService.getLeaderboard();
```

### 🤖 AIService
Сервис интеграции с AI для персонализации обучения.

**Основные возможности:**
- Создание персональных планов обучения
- Генерация адаптивного контента
- Интеллектуальная валидация тестов
- AI-тьютор для ответов на вопросы
- Персонализированные рекомендации
- Генерация финансовых концепций

**Использование:**
```javascript
import AIService from '@/services/AIService';

// Создание персонального плана
const plan = await AIService.createPersonalPlan(planData);

// Вопрос к AI-тьютору
const response = await AIService.askTutor(question);

// Получение рекомендаций
const recommendations = await AIService.getRecommendations();
```

### 🔍 SearchService
Сервис поиска и рекомендаций с векторным поиском.

**Основные возможности:**
- Семантический поиск по контенту
- Поиск по ключевым словам
- Персонализированные рекомендации
- Поиск связанных концепций
- Автодополнение поиска
- История поиска
- Популярный контент

**Использование:**
```javascript
import SearchService from '@/services/SearchService';

// Семантический поиск
const results = await SearchService.semanticSearch(query, filters);

// Получение рекомендаций
const recommendations = await SearchService.getPersonalizedRecommendations();

// Автодополнение
const suggestions = await SearchService.getSearchSuggestions(query);
```

### 👤 UserService
Сервис управления пользователями и профилями.

**Основные возможности:**
- Управление профилем пользователя
- Настройки и предпочтения
- Статистика обучения
- Достижения пользователя
- Дашборд пользователя
- Уведомления
- Экспорт данных

**Использование:**
```javascript
import UserService from '@/services/UserService';

// Получение дашборда
const dashboard = await UserService.getUserDashboard();

// Обновление настроек
await UserService.updateUserPreferences(preferences);

// Получение достижений
const achievements = await UserService.getUserAchievements();
```

### 📊 AnalyticsService
Сервис аналитики и отслеживания пользовательских действий.

**Основные возможности:**
- Отслеживание событий пользователя
- Аналитика обучения и геймификации
- Отслеживание производительности
- Автоматическое отслеживание ошибок
- Управление сессиями
- Экспорт данных аналитики

**Использование:**
```javascript
import AnalyticsService from '@/services/AnalyticsService';

// Отслеживание события
await AnalyticsService.trackEvent('lesson_completed', data);

// Отслеживание просмотра страницы
await AnalyticsService.trackPageView('lessons');

// Получение аналитики
const analytics = await AnalyticsService.getUserAnalytics();
```

### 📱 TelegramService
Сервис интеграции с Telegram (существующий).

**Основные возможности:**
- Интеграция с Telegram Web App
- Отправка уведомлений
- Управление ботом

## Архитектура сервисов

### Принципы проектирования

1. **Единообразие API**: Все сервисы используют async/await и возвращают Promise
2. **Обработка ошибок**: Централизованная обработка ошибок с логированием
3. **Кэширование**: Локальное кэширование данных в localStorage
4. **Реальные API запросы**: Все сервисы работают с реальным backend API
5. **Логирование**: Подробное логирование всех операций

### Взаимодействие сервисов

```
┌─────────────────┐    ┌─────────────────┐
│   Components    │───▶│   Services      │
└─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   ApiService    │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Backend API   │
                       └─────────────────┘
```

### Управление состоянием

- **AuthService**: Управляет состоянием авторизации
- **UserService**: Управляет данными пользователя
- **GamificationService**: Управляет игровыми элементами
- **AnalyticsService**: Отслеживает действия пользователя

## Использование

### Импорт сервисов

```javascript
// Импорт отдельных сервисов
import { AuthService, LessonService } from '@/services';

// Импорт всех сервисов
import Services from '@/services';
const user = await Services.Auth.getCurrentUser();
```

### Инициализация

Сервисы автоматически инициализируются при импорте. Некоторые сервисы (например, AnalyticsService) начинают работу сразу после загрузки.

### Обработка ошибок

```javascript
try {
    const result = await LessonService.getLesson(1);
} catch (error) {
    console.error('Ошибка получения урока:', error);
    // Ошибка автоматически отслеживается AnalyticsService
}
```

## Конфигурация

### Переменные окружения

```env
VUE_APP_API_URL=http://localhost:8000/api/v1
VUE_APP_ENABLE_ANALYTICS=true
```

### Настройки в localStorage

- `auth_token` - JWT токен авторизации
- `user_data` - Данные пользователя
- `user_preferences` - Настройки пользователя
- `user_coins` - Баланс коинов
- `search_history` - История поиска
- `personal_plan` - Персональный план обучения

## Тестирование

### Проверка работоспособности

```javascript
import { ServiceUtils } from '@/services';

// Проверка всех сервисов
const health = await ServiceUtils.checkServicesHealth();
console.log(health);

// Статистика использования
const stats = ServiceUtils.getServicesUsageStats();
console.log(stats);
```

### Очистка данных

```javascript
// Очистка всех данных сервисов
ServiceUtils.clearAllServiceData();

// Экспорт всех данных
ServiceUtils.exportAllServiceData();
```

## Расширение

### Добавление нового сервиса

1. Создайте файл сервиса в `/services/`
2. Импортируйте `ApiService` для HTTP запросов
3. Добавьте экспорт в `index.js`
4. Обновите документацию

### Пример нового сервиса

```javascript
import ApiService from './ApiService';

class NewService {
    async getData() {
        try {
            const response = await ApiService.get('/new-endpoint');
            return response;
        } catch (error) {
            console.error('[NewService] Ошибка:', error);
            throw error;
        }
    }
}

export default new NewService();
```

## Мониторинг

Все сервисы автоматически отслеживаются через AnalyticsService:
- Время выполнения запросов
- Ошибки и исключения
- Использование функций
- Производительность

## Безопасность

- Токены авторизации автоматически добавляются к запросам
- Автоматический logout при истечении токена
- Валидация данных перед отправкой
- Защита от XSS через санитизацию данных

## Производительность

- Локальное кэширование часто используемых данных
- Ленивая загрузка сервисов
- Батчинг аналитических событий
- Оптимизация запросов к API

## Backend API

Все сервисы теперь работают с реальным backend API. Убедитесь, что:

1. Backend сервер запущен и доступен
2. Правильно настроена переменная `VUE_APP_API_URL`
3. API endpoints соответствуют ожидаемым в сервисах
4. Настроена CORS политика на backend

### Основные API endpoints

- `/auth/*` - Авторизация и управление пользователями
- `/lessons/*` - Уроки и обучение
- `/gamification/*` - Геймификация
- `/ai/*` - AI функции
- `/search/*` - Поиск и рекомендации
- `/users/*` - Управление пользователями
- `/analytics/*` - Аналитика 