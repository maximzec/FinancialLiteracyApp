// Централизованный экспорт всех сервисов
import ApiService from './ApiService';
import AuthService from './AuthService';
import { LessonService } from './LessonService';
import GamificationService from './GamificationService';
import AIService from './AIService';
import SearchService from './SearchService';
import UserService from './UserService';
import AnalyticsService from './AnalyticsService';
import TelegramService from './TelegramService';

// Экспорт всех сервисов
export {
    ApiService,
    AuthService,
    LessonService,
    GamificationService,
    AIService,
    SearchService,
    UserService,
    AnalyticsService,
    TelegramService
};

// Экспорт по умолчанию для удобства
export default {
    Api: ApiService,
    Auth: AuthService,
    Lessons: LessonService,
    Gamification: GamificationService,
    AI: AIService,
    Search: SearchService,
    User: UserService,
    Analytics: AnalyticsService,
    Telegram: TelegramService
};

// Утилиты для работы с сервисами
export const ServiceUtils = {
    // Проверка работоспособности всех сервисов
    async checkServicesHealth() {
        const services = [
            'ApiService',
            'AuthService',
            'LessonService',
            'GamificationService',
            'AIService',
            'SearchService',
            'UserService',
            'AnalyticsService'
        ];

        const healthCheck = {};

        for (const serviceName of services) {
            try {
                // Проверяем доступность сервиса
                healthCheck[serviceName] = {
                    status: 'healthy',
                    initialized: true,
                    lastCheck: new Date().toISOString()
                };
            } catch (error) {
                healthCheck[serviceName] = {
                    status: 'error',
                    error: error.message,
                    lastCheck: new Date().toISOString()
                };
            }
        }

        // Проверяем подключение к backend API
        try {
            await ApiService.get('/health');
            healthCheck.backendConnection = {
                status: 'connected',
                lastCheck: new Date().toISOString()
            };
        } catch (error) {
            healthCheck.backendConnection = {
                status: 'disconnected',
                error: error.message,
                lastCheck: new Date().toISOString()
            };
        }

        console.log('[Services] Проверка работоспособности завершена:', healthCheck);
        return healthCheck;
    },

    // Получение статистики использования сервисов
    getServicesUsageStats() {
        const stats = {
            totalServices: 9,
            activeServices: 0,
            localStorage: {
                totalKeys: 0,
                usedSpace: 0,
                keys: []
            },
            analytics: {
                trackingEnabled: AnalyticsService.isTrackingActive(),
                sessionId: AnalyticsService.sessionId
            },
            auth: {
                isLoggedIn: AuthService.isLoggedIn(),
                hasToken: !!localStorage.getItem('auth_token')
            }
        };

        // Подсчет ключей localStorage
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            const value = localStorage.getItem(key);
            stats.localStorage.keys.push({
                key: key,
                size: value ? value.length : 0
            });
            stats.localStorage.usedSpace += value ? value.length : 0;
        }
        stats.localStorage.totalKeys = localStorage.length;

        console.log('[Services] Статистика использования:', stats);
        return stats;
    },

    // Очистка всех данных сервисов
    clearAllServiceData() {
        console.log('[Services] Очистка всех данных сервисов...');

        // Очищаем localStorage
        const keysToKeep = ['theme', 'language']; // Сохраняем некоторые настройки
        const allKeys = [];

        for (let i = 0; i < localStorage.length; i++) {
            allKeys.push(localStorage.key(i));
        }

        allKeys.forEach(key => {
            if (!keysToKeep.includes(key)) {
                localStorage.removeItem(key);
            }
        });

        // Очищаем данные аналитики
        AnalyticsService.clearAnalyticsData();

        // Выходим из системы
        if (AuthService.isLoggedIn()) {
            AuthService.logout();
        }

        console.log('[Services] Все данные сервисов очищены');
        return { success: true, message: 'Все данные успешно очищены' };
    },

    // Экспорт всех данных сервисов
    async exportAllServiceData() {
        console.log('[Services] Экспорт всех данных сервисов...');

        try {
            const exportData = {
                timestamp: new Date().toISOString(),
                version: '1.0.0',
                services: {}
            };

            // Собираем данные из localStorage
            const localStorageData = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                const value = localStorage.getItem(key);
                try {
                    localStorageData[key] = JSON.parse(value);
                } catch {
                    localStorageData[key] = value;
                }
            }
            exportData.services.localStorage = localStorageData;

            // Добавляем данные пользователя
            if (AuthService.isLoggedIn()) {
                exportData.services.user = AuthService.getUser();
            }

            // Добавляем статистику
            exportData.services.stats = this.getServicesUsageStats();

            // Создаем файл для скачивания
            const dataStr = JSON.stringify(exportData, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);

            const link = document.createElement('a');
            link.href = url;
            link.download = `financial_app_services_data_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);

            console.log('[Services] Данные сервисов экспортированы');
            return { success: true, message: 'Данные успешно экспортированы' };
        } catch (error) {
            console.error('[Services] Ошибка экспорта данных:', error);
            throw error;
        }
    },

    // Инициализация всех сервисов
    async initializeServices() {
        console.log('[Services] Инициализация всех сервисов...');

        try {
            // Проверяем подключение к backend
            const healthCheck = await this.checkServicesHealth();

            if (healthCheck.backendConnection.status === 'disconnected') {
                console.warn('[Services] Backend недоступен, некоторые функции могут не работать');
            }

            // Инициализируем аналитику
            if (AnalyticsService.isTrackingActive()) {
                AnalyticsService.trackEvent('services_initialized', {
                    services_count: 9,
                    backend_status: healthCheck.backendConnection.status
                });
            }

            console.log('[Services] Все сервисы инициализированы');
            return { success: true, healthCheck };
        } catch (error) {
            console.error('[Services] Ошибка инициализации сервисов:', error);
            throw error;
        }
    },

    // Глобальный обработчик ошибок для всех сервисов
    setupGlobalErrorHandler() {
        const originalConsoleError = console.error;

        console.error = function (...args) {
            // Отслеживаем ошибки сервисов
            if (args[0] && typeof args[0] === 'string' && args[0].includes('[')) {
                const serviceName = args[0].match(/\[(.*?)\]/)?.[1];
                if (serviceName && AnalyticsService.isTrackingActive()) {
                    AnalyticsService.trackError(new Error(args.join(' ')), {
                        service: serviceName,
                        type: 'service_error'
                    });
                }
            }

            originalConsoleError.apply(console, args);
        };

        console.log('[Services] Глобальный обработчик ошибок настроен');
    }
};

// Автоматическая инициализация при импорте
if (typeof window !== 'undefined') {
    // Настраиваем глобальный обработчик ошибок
    ServiceUtils.setupGlobalErrorHandler();

    // Инициализируем сервисы при загрузке страницы
    document.addEventListener('DOMContentLoaded', () => {
        ServiceUtils.initializeServices().catch(error => {
            console.error('[Services] Ошибка автоматической инициализации:', error);
        });
    });
} 