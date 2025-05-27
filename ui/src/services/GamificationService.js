import ApiService from './ApiService';

// Сервис геймификации
class GamificationService {
    constructor() {
        this.userCoins = this.loadCoinsFromStorage();
    }

    // Загрузка коинов из localStorage
    loadCoinsFromStorage() {
        const savedCoins = localStorage.getItem('user_coins');
        return savedCoins ? parseInt(savedCoins) : 0;
    }

    // Сохранение коинов в localStorage
    saveCoinsToStorage(coins) {
        localStorage.setItem('user_coins', coins.toString());
        this.userCoins = coins;
    }

    // Получение баланса коинов пользователя
    async getUserCoins() {
        try {
            console.log('[Gamification] Получение баланса коинов');

            const response = await ApiService.get('/gamification/coins');

            // Обновляем локальный кэш
            if (response.current_balance !== undefined) {
                this.saveCoinsToStorage(response.current_balance);
            }

            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения коинов:', error);
            throw error;
        }
    }

    // Добавление коинов за активность
    async addCoins(amount, reason = 'Активность') {
        try {
            console.log(`[Gamification] Добавление ${amount} коинов за: ${reason}`);

            const response = await ApiService.post('/gamification/coins/add', {
                amount: amount,
                reason: reason
            });

            // Обновляем локальный баланс
            if (response.new_balance !== undefined) {
                this.saveCoinsToStorage(response.new_balance);
            }

            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка добавления коинов:', error);
            throw error;
        }
    }

    // Трата коинов
    async spendCoins(amount, reason = 'Покупка') {
        try {
            console.log(`[Gamification] Трата ${amount} коинов на: ${reason}`);

            const response = await ApiService.post('/gamification/coins/spend', {
                amount: amount,
                reason: reason
            });

            // Обновляем локальный баланс
            if (response.new_balance !== undefined) {
                this.saveCoinsToStorage(response.new_balance);
            }

            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка траты коинов:', error);
            throw error;
        }
    }

    // Получение списка челленджей
    async getChallenges(filters = {}) {
        try {
            console.log('[Gamification] Получение списка челленджей');

            const response = await ApiService.get('/gamification/challenges', filters);
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения челленджей:', error);
            throw error;
        }
    }

    // Присоединение к челленджу
    async joinChallenge(challengeId) {
        try {
            console.log(`[Gamification] Присоединение к челленджу ${challengeId}`);

            const response = await ApiService.post(`/gamification/challenges/${challengeId}/join`);
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка присоединения к челленджу:', error);
            throw error;
        }
    }

    // Получение челленджей пользователя
    async getUserChallenges(status = null) {
        try {
            console.log('[Gamification] Получение челленджей пользователя');

            const params = {};
            if (status) {
                params.status = status;
            }

            const response = await ApiService.get('/gamification/user-challenges', params);
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения челленджей пользователя:', error);
            throw error;
        }
    }

    // Обновление прогресса челленджа
    async updateChallengeProgress(challengeId, progress) {
        try {
            console.log(`[Gamification] Обновление прогресса челленджа ${challengeId}:`, progress);

            const response = await ApiService.put(`/gamification/challenges/${challengeId}/progress`, {
                progress: progress
            });

            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка обновления прогресса:', error);
            throw error;
        }
    }

    // Завершение челленджа
    async completeChallenge(challengeId) {
        try {
            console.log(`[Gamification] Завершение челленджа ${challengeId}`);

            const response = await ApiService.post(`/gamification/challenges/${challengeId}/complete`);
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка завершения челленджа:', error);
            throw error;
        }
    }

    // Получение статистики геймификации
    async getGamificationStats() {
        try {
            console.log('[Gamification] Получение статистики геймификации');

            const response = await ApiService.get('/gamification/stats');
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения статистики:', error);
            throw error;
        }
    }

    // Получение таблицы лидеров
    async getLeaderboard(limit = 10, period = 'all') {
        try {
            console.log('[Gamification] Получение таблицы лидеров');

            const response = await ApiService.get('/gamification/leaderboard', {
                limit: limit,
                period: period
            });

            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения лидерборда:', error);
            throw error;
        }
    }

    // Получение достижений пользователя
    async getUserAchievements() {
        try {
            console.log('[Gamification] Получение достижений пользователя');

            const response = await ApiService.get('/gamification/achievements');
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения достижений:', error);
            throw error;
        }
    }

    // Получение массовых событий
    async getMassEvents() {
        try {
            console.log('[Gamification] Получение массовых событий');

            const response = await ApiService.get('/gamification/mass-events');
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения массовых событий:', error);
            throw error;
        }
    }

    // Присоединение к массовому событию
    async joinMassEvent(eventId) {
        try {
            console.log(`[Gamification] Присоединение к массовому событию ${eventId}`);

            const response = await ApiService.post(`/gamification/mass-events/${eventId}/join`);
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка присоединения к событию:', error);
            throw error;
        }
    }

    // Получение истории транзакций коинов
    async getCoinTransactions(limit = 20, transactionType = null) {
        try {
            console.log('[Gamification] Получение истории транзакций коинов');

            const params = { limit };
            if (transactionType) {
                params.transaction_type = transactionType;
            }

            const response = await ApiService.get('/gamification/coin-transactions', params);
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения транзакций:', error);
            throw error;
        }
    }

    // Получение доступных наград
    async getAvailableRewards() {
        try {
            console.log('[Gamification] Получение доступных наград');

            const response = await ApiService.get('/gamification/rewards');
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения наград:', error);
            throw error;
        }
    }

    // Покупка награды
    async purchaseReward(rewardId) {
        try {
            console.log(`[Gamification] Покупка награды ${rewardId}`);

            const response = await ApiService.post(`/gamification/rewards/${rewardId}/purchase`);

            // Обновляем локальный баланс
            if (response.new_balance !== undefined) {
                this.saveCoinsToStorage(response.new_balance);
            }

            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка покупки награды:', error);
            throw error;
        }
    }

    // Получение рейтинга пользователя
    async getUserRank() {
        try {
            console.log('[Gamification] Получение рейтинга пользователя');

            const response = await ApiService.get('/gamification/user-rank');
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения рейтинга:', error);
            throw error;
        }
    }

    // Получение ежедневных заданий
    async getDailyTasks() {
        try {
            console.log('[Gamification] Получение ежедневных заданий');

            const response = await ApiService.get('/gamification/daily-tasks');
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка получения ежедневных заданий:', error);
            throw error;
        }
    }

    // Завершение ежедневного задания
    async completeDailyTask(taskId) {
        try {
            console.log(`[Gamification] Завершение ежедневного задания ${taskId}`);

            const response = await ApiService.post(`/gamification/daily-tasks/${taskId}/complete`);
            return response;
        } catch (error) {
            console.error('[Gamification] Ошибка завершения задания:', error);
            throw error;
        }
    }
}

export default new GamificationService(); 