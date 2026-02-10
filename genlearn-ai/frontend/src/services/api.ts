/**
 * API Service - Centralized API communication layer
 *
 * All API calls go through this service.
 * Base URL and authentication are handled here.
 */

import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
// Backend base URL without /api suffix - used for static file URLs (images, media)
export const BACKEND_URL = API_BASE_URL.replace(/\/api\/?$/, '');
const API_KEY = 'kd_dreaming007'; // Application API key

class ApiService {
  public client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY, // Add API key to all requests
      },
    });

    // Request interceptor - add auth token and API key
    this.client.interceptors.request.use((config) => {
      // Always add API key to headers
      config.headers['X-API-Key'] = API_KEY;

      // Add auth token if available
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Response interceptor - handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // ============================================================
  // AUTHENTICATION
  // ============================================================

  async login(username: string, password: string) {
    const response = await this.client.post('/auth/login', { username, password });
    return response.data;
  }

  async logout() {
    localStorage.removeItem('auth_token');
  }

  async getCurrentUser() {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  // ============================================================
  // LEARNING
  // ============================================================

  async startSession(config: {
    topic: string;
    difficulty_level: number;
    duration_minutes: number;
    visual_style: 'cartoon' | 'realistic';
    story_style?: string;
    play_mode: 'solo' | 'team' | 'tournament';
    avatar_id?: string;
    character_ids?: string[];
    team_id?: string;
    tournament_id?: string;
  }) {
    const response = await this.client.post('/learning/start', config);
    return response.data;
  }

  async getSessionContent(sessionId: string) {
    const response = await this.client.get(`/learning/session/${sessionId}/content`);
    return response.data;
  }

  async submitProgress(sessionId: string, data: any) {
    const response = await this.client.post(`/learning/session/${sessionId}/progress`, data);
    return response.data;
  }

  async endSession(sessionId: string, finalScore: number = 0, totalTimeSeconds: number = 0, completed: boolean = true) {
    const response = await this.client.post(`/learning/session/${sessionId}/end`, {
      final_score: finalScore,
      total_time_seconds: totalTimeSeconds,
      completed,
    });
    return response.data;
  }

  async getSessionHistory(limit: number = 20, offset: number = 0) {
    const response = await this.client.get(`/learning/history?limit=${limit}&offset=${offset}`);
    return response.data;
  }

  async getSessionRevision(sessionId: string) {
    const response = await this.client.get(`/learning/history/${sessionId}`);
    return response.data;
  }

  // ============================================================
  // QUIZ
  // ============================================================

  async getMCQQuestions(sessionId: string) {
    const response = await this.client.get(`/quiz/session/${sessionId}/mcq`);
    return response.data;
  }

  async submitMCQAnswer(sessionId: string, questionId: string, answer: string) {
    const response = await this.client.post(`/quiz/session/${sessionId}/mcq/answer`, {
      question_id: questionId,
      answer,
    });
    return response.data;
  }

  async getDescriptiveQuestions(sessionId: string) {
    const response = await this.client.get(`/quiz/session/${sessionId}/descriptive`);
    return response.data;
  }

  async submitDescriptiveAnswer(sessionId: string, questionId: string, answer: string) {
    const response = await this.client.post(`/quiz/session/${sessionId}/descriptive/answer`, {
      question_id: questionId,
      answer,
    });
    return response.data;
  }

  // ============================================================
  // AVATAR & CHARACTERS
  // ============================================================

  async getAvatars() {
    const response = await this.client.get('/avatar/list');
    return response.data;
  }

  async createAvatarFromUpload(file: File, name: string, style: string, customPrompt: string = '') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    formData.append('style', style);
    formData.append('custom_prompt', customPrompt);
    const response = await this.client.post('/avatar/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async createAvatarFromDrawing(drawingData: string, name: string, style: string, customPrompt: string = '') {
    const response = await this.client.post('/avatar/draw', {
      drawing_data: drawingData,
      name,
      style,
      custom_prompt: customPrompt,
    });
    return response.data;
  }

  async getCharacters() {
    const response = await this.client.get('/characters/list');
    return response.data;
  }

  async createCharacter(file: File, name: string, description: string) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    formData.append('description', description);
    const response = await this.client.post('/characters/create', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async createCharacterFromUpload(
    file: File,
    name: string,
    description: string,
    style: string,
    customPrompt: string = ''
  ) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', name);
    formData.append('description', description);
    formData.append('style', style);
    formData.append('custom_prompt', customPrompt);
    const response = await this.client.post('/characters/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async createCharacterFromDrawing(
    drawingData: string,
    name: string,
    description: string,
    style: string,
    customPrompt: string = ''
  ) {
    const response = await this.client.post('/characters/draw', {
      drawing_data: drawingData,
      name,
      description,
      style,
      custom_prompt: customPrompt,
    });
    return response.data;
  }

  // ============================================================
  // VOICE
  // ============================================================

  async textToSpeech(text: string, language: string, voiceType: string) {
    const response = await this.client.post('/voice/tts', {
      text,
      language,
      voice_type: voiceType,
    }, { responseType: 'blob' });
    return response.data;
  }

  async speechToText(audioBlob: Blob, language: string) {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    formData.append('language', language);
    const response = await this.client.post('/voice/stt', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  // ============================================================
  // VIDEO - DISABLED FOR MVP
  // ============================================================
  // Video generation has been disabled. These methods are commented out.

  // async getVideo(sessionId: string, cycleNumber: number) {
  //   const response = await this.client.get(`/video/session/${sessionId}/cycle/${cycleNumber}`);
  //   return response.data;
  // }

  // async checkVideoStatus(sessionId: string, cycleNumber: number) {
  //   const response = await this.client.get(`/video/session/${sessionId}/cycle/${cycleNumber}/status`);
  //   return response.data;
  // }

  // ============================================================
  // TOURNAMENTS & TEAMS
  // ============================================================

  async getTournaments(status?: string) {
    const params = status ? { status } : {};
    const response = await this.client.get('/tournaments/list', { params });
    return response.data;
  }

  async joinTournament(tournamentId: string, teamId?: string) {
    const response = await this.client.post(`/tournaments/${tournamentId}/join`, { team_id: teamId });
    return response.data;
  }

  async getTeams() {
    const response = await this.client.get('/teams/list');
    return response.data;
  }

  async createTeam(name: string) {
    const response = await this.client.post('/teams/create', { name });
    return response.data;
  }

  async joinTeam(teamId: string) {
    const response = await this.client.post(`/teams/${teamId}/join`);
    return response.data;
  }

  async getLeaderboard(scope?: 'global' | 'tournament', tournamentId?: string) {
    const params: any = {};
    if (scope) params.scope = scope;
    if (tournamentId) params.tournament_id = tournamentId;
    const response = await this.client.get('/tournaments/leaderboard', { params });
    return response.data;
  }

  // ============================================================
  // CHAT
  // ============================================================

  async sendChatMessage(message: string, context?: string, language?: string) {
    const response = await this.client.post('/chat/message', {
      message,
      context,
      language,
    });
    return response.data;
  }

  // ============================================================
  // ADMIN
  // ============================================================

  async createTournament(data: any) {
    const response = await this.client.post('/admin/tournaments/create', data);
    return response.data;
  }

  async uploadQuestions(file: File, questionType: 'mcq' | 'descriptive') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('question_type', questionType);
    const response = await this.client.post('/admin/questions/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async getUsers() {
    const response = await this.client.get('/admin/users');
    return response.data;
  }

  // ============================================================
  // HISTORY & PROFILE
  // ============================================================

  async getLearningHistory() {
    const response = await this.client.get('/users/history');
    return response.data;
  }

  async updateProfile(data: any) {
    const response = await this.client.put('/users/profile', data);
    return response.data;
  }

  async updateSettings(data: any) {
    const response = await this.client.put('/users/settings', data);
    return response.data;
  }

  // ============================================================
  // GENERIC HTTP METHODS (for direct access)
  // ============================================================

  async get(url: string, config?: any) {
    return this.client.get(url, config);
  }

  async post(url: string, data?: any, config?: any) {
    return this.client.post(url, data, config);
  }

  async put(url: string, data?: any, config?: any) {
    return this.client.put(url, data, config);
  }

  async delete(url: string, config?: any) {
    return this.client.delete(url, config);
  }
}

export const api = new ApiService();
export default api;
