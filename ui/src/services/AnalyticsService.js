import ApiService from './ApiService';

// Сервис аналитики и отслеживания
class AnalyticsService {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.events = [];
        this.isTrackingEnabled = this.getTrackingPreference();
        this.startSession();
    }

    // Генерация ID сессии
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    // Получение настройки отслеживания
    getTrackingPreference() {
        const preferences = localStorage.getItem('user_preferences');
        if (preferences) {
            const parsed = JSON.parse(preferences);
            return parsed.privacy?.data_analytics !== false;
        }
        return true; // По умолчанию включено
    }

    // Начало сессии
    startSession() {
        if (!this.isTrackingEnabled) return;

        const sessionData = {
            session_id: this.sessionId,
            started_at: new Date().toISOString(),
            user_agent: navigator.userAgent,
            screen_resolution: `${screen.width}x${screen.height}`,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            language: navigator.language
        };

        this.trackEvent('session_start', sessionData);
        console.log('[Analytics] Сессия начата:', this.sessionId);
    }

    // Завершение сессии
    endSession() {
        if (!this.isTrackingEnabled) return;

        const sessionData = {
            session_id: this.sessionId,
            ended_at: new Date().toISOString(),
            duration_seconds: this.getSessionDuration(),
            events_count: this.events.length
        };

        this.trackEvent('session_end', sessionData);
        this.sendPendingEvents();
        console.log('[Analytics] Сессия завершена:', this.sessionId);
    }

    // Получение длительности сессии
    getSessionDuration() {
        const sessionStart = this.events.find(e => e.event_type === 'session_start');
        if (sessionStart) {
            return Math.floor((Date.now() - new Date(sessionStart.timestamp).getTime()) / 1000);
        }
        return 0;
    }

    // Основной метод отслеживания событий
    async trackEvent(eventType, eventData = {}, immediate = false) {
        if (!this.isTrackingEnabled) return;

        try {
            const event = {
                id: Math.floor(Math.random() * 1000000),
                session_id: this.sessionId,
                event_type: eventType,
                event_data: eventData,
                timestamp: new Date().toISOString(),
                url: window.location.href,
                referrer: document.referrer
            };

            this.events.push(event);
            console.log(`[Analytics] Событие отслежено: ${eventType}`, event);

            // Отправляем немедленно для критических событий
            if (immediate) {
                await this.sendEvent(event);
            }

            // Автоматическая отправка при накоплении событий
            if (this.events.length >= 10) {
                await this.sendPendingEvents();
            }

            return event;
        } catch (error) {
            console.error('[Analytics] Ошибка отслеживания события:', error);
        }
    }

    // Отслеживание просмотра страницы
    async trackPageView(pageName, pageData = {}) {
        return this.trackEvent('page_view', {
            page_name: pageName,
            page_title: document.title,
            ...pageData
        });
    }

    // Отслеживание действий пользователя
    async trackUserAction(action, actionData = {}) {
        return this.trackEvent('user_action', {
            action: action,
            ...actionData
        });
    }

    // Отслеживание обучения
    async trackLearningEvent(eventType, lessonData = {}) {
        return this.trackEvent('learning_event', {
            learning_event_type: eventType,
            ...lessonData
        });
    }

    // Отслеживание геймификации
    async trackGamificationEvent(eventType, gamificationData = {}) {
        return this.trackEvent('gamification_event', {
            gamification_event_type: eventType,
            ...gamificationData
        });
    }

    // Отслеживание ошибок
    async trackError(error, context = {}) {
        return this.trackEvent('error', {
            error_message: error.message,
            error_stack: error.stack,
            error_type: error.constructor.name,
            context: context
        }, true); // Отправляем ошибки немедленно
    }

    // Отслеживание производительности
    async trackPerformance(metricName, value, unit = 'ms') {
        return this.trackEvent('performance', {
            metric_name: metricName,
            value: value,
            unit: unit
        });
    }

    // Отслеживание поиска
    async trackSearch(query, results = {}) {
        return this.trackEvent('search', {
            search_query: query,
            results_count: results.count || 0,
            search_type: results.type || 'general',
            filters_applied: results.filters || {}
        });
    }

    // Отслеживание конверсий
    async trackConversion(conversionType, conversionData = {}) {
        return this.trackEvent('conversion', {
            conversion_type: conversionType,
            ...conversionData
        }, true); // Конверсии отправляем немедленно
    }

    // Отправка одного события
    async sendEvent(event) {
        try {
            console.log('[Analytics] Отправка события на backend:', event);

            const response = await ApiService.post('/analytics/events', {
                events: [event]
            });

            return { success: true };
        } catch (error) {
            console.error('[Analytics] Ошибка отправки события:', error);
            return { success: false, error: error.message };
        }
    }

    // Отправка накопленных событий
    async sendPendingEvents() {
        if (this.events.length === 0) return;

        try {
            console.log(`[Analytics] Отправка ${this.events.length} событий на backend`);

            const response = await ApiService.post('/analytics/events', {
                events: this.events
            });

            // Очищаем отправленные события
            this.events = [];

            return { success: true, sent_count: this.events.length };
        } catch (error) {
            console.error('[Analytics] Ошибка отправки событий:', error);
            return { success: false, error: error.message };
        }
    }

    // Получение аналитики пользователя
    async getUserAnalytics(period = 'week') {
        try {
            console.log(`[Analytics] Получение аналитики пользователя за ${period}`);

            const response = await ApiService.get('/analytics/user', {
                period: period
            });

            // Имитация аналитики пользователя
            const mockAnalytics = {
                period: period,
                total_sessions: 15,
                total_time_spent: 1250, // минуты
                average_session_duration: 83, // минуты
                pages_visited: 45,
                actions_performed: 120,
                learning_events: {
                    lessons_started: 8,
                    lessons_completed: 5,
                    quizzes_taken: 12,
                    correct_answers: 9
                },
                gamification_events: {
                    coins_earned: 275,
                    challenges_joined: 2,
                    challenges_completed: 1,
                    achievements_earned: 3
                },
                popular_pages: [
                    { page: '/lessons', visits: 12 },
                    { page: '/dashboard', visits: 8 },
                    { page: '/challenges', visits: 6 },
                    { page: '/profile', visits: 4 }
                ],
                device_info: {
                    desktop: 70,
                    mobile: 25,
                    tablet: 5
                },
                engagement_score: 0.78
            };

            return mockAnalytics;
        } catch (error) {
            console.error('[Analytics] Ошибка получения аналитики:', error);
            return null;
        }
    }

    // Получение общей аналитики приложения
    async getAppAnalytics(period = 'week') {
        try {
            console.log(`[Analytics] Получение общей аналитики за ${period}`);

            const response = await ApiService.get('/analytics/app', {
                period: period
            });

            // Имитация общей аналитики
            const mockAppAnalytics = {
                period: period,
                total_users: 3250,
                active_users: 1890,
                new_users: 245,
                returning_users: 1645,
                total_sessions: 8750,
                average_session_duration: 67, // минуты
                bounce_rate: 0.23,
                conversion_rate: 0.15,
                popular_content: [
                    { type: 'lesson', id: 1, title: 'Основы личного бюджета', views: 1250 },
                    { type: 'lesson', id: 2, title: 'Основы инвестирования', views: 980 },
                    { type: 'challenge', id: 1, title: 'Первые шаги', participants: 650 }
                ],
                user_flow: [
                    { step: 'Landing', users: 3250, conversion: 1.0 },
                    { step: 'Registration', users: 2600, conversion: 0.8 },
                    { step: 'Profile Setup', users: 2080, conversion: 0.8 },
                    { step: 'First Lesson', users: 1560, conversion: 0.75 },
                    { step: 'Lesson Completion', users: 936, conversion: 0.6 }
                ],
                retention: {
                    day_1: 0.85,
                    day_7: 0.62,
                    day_30: 0.34
                }
            };

            return mockAppAnalytics;
        } catch (error) {
            console.error('[Analytics] Ошибка получения общей аналитики:', error);
            return null;
        }
    }

    // Создание пользовательского события
    async createCustomEvent(eventName, eventData = {}) {
        return this.trackEvent('custom_event', {
            custom_event_name: eventName,
            ...eventData
        });
    }

    // Отслеживание времени на странице
    startPageTimer(pageName) {
        this.pageStartTime = Date.now();
        this.currentPage = pageName;
    }

    endPageTimer() {
        if (this.pageStartTime && this.currentPage) {
            const timeSpent = Date.now() - this.pageStartTime;
            this.trackPerformance(`page_time_${this.currentPage}`, timeSpent);
            this.pageStartTime = null;
            this.currentPage = null;
        }
    }

    // Отслеживание кликов
    trackClick(element, elementData = {}) {
        return this.trackUserAction('click', {
            element_type: element.tagName,
            element_id: element.id,
            element_class: element.className,
            element_text: element.textContent?.substring(0, 100),
            ...elementData
        });
    }

    // Отслеживание скролла
    trackScroll(scrollPercentage) {
        return this.trackUserAction('scroll', {
            scroll_percentage: scrollPercentage,
            page_height: document.body.scrollHeight,
            viewport_height: window.innerHeight
        });
    }

    // Отслеживание форм
    trackFormSubmission(formName, formData = {}) {
        return this.trackUserAction('form_submit', {
            form_name: formName,
            form_fields: Object.keys(formData).length,
            ...formData
        });
    }

    // Отслеживание загрузки файлов
    trackFileUpload(fileName, fileSize, fileType) {
        return this.trackUserAction('file_upload', {
            file_name: fileName,
            file_size: fileSize,
            file_type: fileType
        });
    }

    // Отслеживание видео
    trackVideoEvent(videoId, eventType, currentTime = 0, duration = 0) {
        return this.trackUserAction('video_event', {
            video_id: videoId,
            video_event_type: eventType, // play, pause, complete, etc.
            current_time: currentTime,
            duration: duration,
            progress_percentage: duration > 0 ? (currentTime / duration) * 100 : 0
        });
    }

    // Включение/отключение отслеживания
    setTrackingEnabled(enabled) {
        this.isTrackingEnabled = enabled;

        // Сохраняем настройку
        const preferences = JSON.parse(localStorage.getItem('user_preferences') || '{}');
        if (!preferences.privacy) preferences.privacy = {};
        preferences.privacy.data_analytics = enabled;
        localStorage.setItem('user_preferences', JSON.stringify(preferences));

        console.log(`[Analytics] Отслеживание ${enabled ? 'включено' : 'отключено'}`);
    }

    // Получение статуса отслеживания
    isTrackingActive() {
        return this.isTrackingEnabled;
    }

    // Очистка данных аналитики
    clearAnalyticsData() {
        this.events = [];
        console.log('[Analytics] Данные аналитики очищены');
    }

    // Экспорт данных аналитики
    exportAnalyticsData() {
        const analyticsData = {
            session_id: this.sessionId,
            events: this.events,
            exported_at: new Date().toISOString()
        };

        const dataStr = JSON.stringify(analyticsData, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);

        const link = document.createElement('a');
        link.href = url;
        link.download = `analytics_data_${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        console.log('[Analytics] Данные аналитики экспортированы');
    }

    // Автоматическое отслеживание при закрытии страницы
    setupAutoTracking() {
        // Отслеживание закрытия страницы
        window.addEventListener('beforeunload', () => {
            this.endPageTimer();
            this.endSession();
        });

        // Отслеживание изменения видимости страницы
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.trackUserAction('page_hidden');
            } else {
                this.trackUserAction('page_visible');
            }
        });

        // Отслеживание ошибок JavaScript
        window.addEventListener('error', (event) => {
            this.trackError(event.error, {
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno
            });
        });

        // Отслеживание необработанных промисов
        window.addEventListener('unhandledrejection', (event) => {
            this.trackError(new Error(event.reason), {
                type: 'unhandled_promise_rejection'
            });
        });

        console.log('[Analytics] Автоматическое отслеживание настроено');
    }
}

// Создаем глобальный экземпляр и настраиваем автоматическое отслеживание
const analyticsService = new AnalyticsService();
analyticsService.setupAutoTracking();

export default analyticsService; 