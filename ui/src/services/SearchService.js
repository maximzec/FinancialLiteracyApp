import ApiService from './ApiService';

// Сервис поиска и рекомендаций
class SearchService {
    constructor() {
        this.searchHistory = this.loadSearchHistory();
        this.recentSearches = [];
    }

    // Загрузка истории поиска из localStorage
    loadSearchHistory() {
        const saved = localStorage.getItem('search_history');
        return saved ? JSON.parse(saved) : [];
    }

    // Сохранение истории поиска
    saveSearchHistory() {
        localStorage.setItem('search_history', JSON.stringify(this.searchHistory));
    }

    // Семантический поиск
    async semanticSearch(query, filters = {}) {
        try {
            console.log('[Search] Семантический поиск:', query);

            const response = await ApiService.post('/search/semantic', {
                query: query,
                content_types: filters.contentTypes,
                categories: filters.categories,
                difficulty_levels: filters.difficultyLevels,
                limit: filters.limit || 10
            });

            // Сохраняем поиск в историю
            this.addToSearchHistory(query, response.length || 0);

            return response;
        } catch (error) {
            console.error('[Search] Ошибка семантического поиска:', error);
            throw error;
        }
    }

    // Поиск по ключевым словам
    async keywordSearch(keywords, filters = {}) {
        try {
            console.log('[Search] Поиск по ключевым словам:', keywords);

            const response = await ApiService.get('/search/keywords', {
                keywords: keywords,
                ...filters
            });

            return response;
        } catch (error) {
            console.error('[Search] Ошибка поиска по ключевым словам:', error);
            throw error;
        }
    }

    // Получение персонализированных рекомендаций
    async getPersonalizedRecommendations(limit = 5) {
        try {
            console.log('[Search] Получение персонализированных рекомендаций');

            const response = await ApiService.get('/search/recommendations', { limit });
            return response;
        } catch (error) {
            console.error('[Search] Ошибка получения рекомендаций:', error);
            throw error;
        }
    }

    // Поиск связанных концепций
    async findRelatedConcepts(conceptId) {
        try {
            console.log(`[Search] Поиск связанных концепций для ${conceptId}`);

            const response = await ApiService.get(`/search/concepts/${conceptId}`);
            return response;
        } catch (error) {
            console.error('[Search] Ошибка поиска связанных концепций:', error);
            throw error;
        }
    }

    // Добавление контента в базу знаний
    async addToKnowledgeBase(knowledgeData) {
        try {
            console.log('[Search] Добавление в базу знаний:', knowledgeData);

            const response = await ApiService.post('/search/knowledge-base', {
                title: knowledgeData.title,
                content: knowledgeData.content,
                content_type: knowledgeData.contentType,
                category: knowledgeData.category,
                difficulty_level: knowledgeData.difficultyLevel,
                tags: knowledgeData.tags,
                source: knowledgeData.source
            });

            return response;
        } catch (error) {
            console.error('[Search] Ошибка добавления в базу знаний:', error);
            throw error;
        }
    }

    // Получение популярного контента
    async getTrendingContent(period = 'week', limit = 10) {
        try {
            console.log(`[Search] Получение популярного контента за ${period}`);

            const response = await ApiService.get('/search/trending', {
                period: period,
                limit: limit
            });

            return response;
        } catch (error) {
            console.error('[Search] Ошибка получения популярного контента:', error);
            throw error;
        }
    }

    // Получение статистики поиска
    async getSearchStats() {
        try {
            console.log('[Search] Получение статистики поиска');

            const response = await ApiService.get('/search/stats');
            return response;
        } catch (error) {
            console.error('[Search] Ошибка получения статистики:', error);
            throw error;
        }
    }

    // Автодополнение поиска
    async getSearchSuggestions(query, limit = 5) {
        try {
            console.log(`[Search] Получение предложений для: ${query}`);

            const response = await ApiService.get('/search/suggestions', {
                query: query,
                limit: limit
            });

            return response;
        } catch (error) {
            console.error('[Search] Ошибка получения предложений:', error);
            throw error;
        }
    }

    // Сохранение взаимодействия с поиском
    async trackSearchInteraction(interactionData) {
        try {
            console.log('[Search] Отслеживание взаимодействия:', interactionData);

            const response = await ApiService.post('/search/interactions', {
                interaction_type: interactionData.type,
                content_type: interactionData.contentType,
                content_id: interactionData.contentId,
                query: interactionData.query,
                duration_seconds: interactionData.duration,
                rating: interactionData.rating
            });

            return response;
        } catch (error) {
            console.error('[Search] Ошибка отслеживания взаимодействия:', error);
            return { success: false };
        }
    }

    // Получение истории поиска
    getSearchHistory() {
        return this.searchHistory;
    }

    // Добавление в историю поиска
    addToSearchHistory(query, resultsCount) {
        const searchEntry = {
            id: Date.now(),
            query: query,
            results_count: resultsCount,
            timestamp: new Date().toISOString()
        };

        this.searchHistory.unshift(searchEntry);

        // Ограничиваем историю 50 записями
        if (this.searchHistory.length > 50) {
            this.searchHistory = this.searchHistory.slice(0, 50);
        }

        this.saveSearchHistory();
    }

    // Очистка истории поиска
    clearSearchHistory() {
        this.searchHistory = [];
        this.saveSearchHistory();
    }

    // Получение популярных запросов пользователя
    getPopularUserQueries(limit = 10) {
        const queryCount = {};

        this.searchHistory.forEach(entry => {
            queryCount[entry.query] = (queryCount[entry.query] || 0) + 1;
        });

        return Object.entries(queryCount)
            .sort(([, a], [, b]) => b - a)
            .slice(0, limit)
            .map(([query, count]) => ({ query, count }));
    }

    // Фильтрация результатов поиска
    filterResults(results, filters) {
        return results.filter(result => {
            if (filters.contentTypes && !filters.contentTypes.includes(result.content_type)) {
                return false;
            }
            if (filters.categories && !filters.categories.includes(result.category)) {
                return false;
            }
            if (filters.difficultyLevels && !filters.difficultyLevels.includes(result.difficulty_level)) {
                return false;
            }
            if (filters.minSimilarity && result.similarity < filters.minSimilarity) {
                return false;
            }
            return true;
        });
    }

    // Сортировка результатов поиска
    sortResults(results, sortBy = 'similarity') {
        return results.sort((a, b) => {
            switch (sortBy) {
                case 'similarity':
                    return (b.similarity || 0) - (a.similarity || 0);
                case 'relevance':
                    return (b.relevance || 0) - (a.relevance || 0);
                case 'date':
                    return new Date(b.created_at || 0) - new Date(a.created_at || 0);
                case 'popularity':
                    return (b.views || 0) - (a.views || 0);
                default:
                    return 0;
            }
        });
    }

    // Глобальный поиск
    async globalSearch(query, options = {}) {
        try {
            console.log('[Search] Глобальный поиск:', query);

            const response = await ApiService.get('/search/global', {
                query: query,
                include_lessons: options.includeLessons !== false,
                include_challenges: options.includeChallenges !== false,
                include_articles: options.includeArticles !== false,
                limit: options.limit || 20
            });

            // Сохраняем поиск в историю
            this.addToSearchHistory(query, response.total_results || 0);

            return response;
        } catch (error) {
            console.error('[Search] Ошибка глобального поиска:', error);
            throw error;
        }
    }

    // Поиск с фильтрами
    async advancedSearch(searchParams) {
        try {
            console.log('[Search] Расширенный поиск:', searchParams);

            const response = await ApiService.post('/search/advanced', searchParams);
            return response;
        } catch (error) {
            console.error('[Search] Ошибка расширенного поиска:', error);
            throw error;
        }
    }

    // Получение похожего контента
    async getSimilarContent(contentId, contentType, limit = 5) {
        try {
            console.log(`[Search] Поиск похожего контента для ${contentType}:${contentId}`);

            const response = await ApiService.get('/search/similar', {
                content_id: contentId,
                content_type: contentType,
                limit: limit
            });

            return response;
        } catch (error) {
            console.error('[Search] Ошибка поиска похожего контента:', error);
            throw error;
        }
    }

    // Сохранение поискового запроса
    async saveSearch(query, filters = {}) {
        try {
            console.log('[Search] Сохранение поискового запроса');

            const response = await ApiService.post('/search/saved-searches', {
                query: query,
                filters: filters,
                name: `Поиск: ${query}`
            });

            return response;
        } catch (error) {
            console.error('[Search] Ошибка сохранения поиска:', error);
            throw error;
        }
    }

    // Получение сохраненных поисков
    async getSavedSearches() {
        try {
            console.log('[Search] Получение сохраненных поисков');

            const response = await ApiService.get('/search/saved-searches');
            return response;
        } catch (error) {
            console.error('[Search] Ошибка получения сохраненных поисков:', error);
            throw error;
        }
    }

    // Удаление сохраненного поиска
    async deleteSavedSearch(searchId) {
        try {
            console.log(`[Search] Удаление сохраненного поиска ${searchId}`);

            const response = await ApiService.delete(`/search/saved-searches/${searchId}`);
            return response;
        } catch (error) {
            console.error('[Search] Ошибка удаления сохраненного поиска:', error);
            throw error;
        }
    }
}

export default new SearchService(); 