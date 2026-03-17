import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';
import { Layout } from './components/layout/Layout';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { LoadingSpinner } from './components/common/LoadingSpinner';
import { LanguageProvider } from './contexts/LanguageContext';

// Pages
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { LearningPage } from './pages/LearningPage';
import { ProfilePage } from './pages/ProfilePage';
import { SettingsPage } from './pages/SettingsPage';
import { HistoryPage } from './pages/HistoryPage';
import { RevisionPage } from './pages/RevisionPage';

// Core Features Pages
import { MistakeAutopsyPage } from './pages/MistakeAutopsyPage';
import { FeynmanEnginePage } from './pages/FeynmanEnginePage';
import StoryLearningPage from './pages/StoryLearningPage';
import { AvatarPage } from './pages/AvatarPage';

// Admin Pages
import { AdminHomePage } from './pages/admin/AdminHomePage';
import { ManageQuestionsPage } from './pages/admin/ManageQuestionsPage';
import { ManageUsersPage } from './pages/admin/ManageUsersPage';


function App() {
  const { loadUser, isLoading } = useAuth();

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading..." />
      </div>
    );
  }

  return (
    <LanguageProvider>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />

          {/* Protected routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Layout>
                  <DashboardPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/learning"
            element={
              <ProtectedRoute>
                <Layout>
                  <LearningPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Layout>
                  <ProfilePage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <Layout>
                  <SettingsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/history"
            element={
              <ProtectedRoute>
                <Layout>
                  <HistoryPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/learning/revision/:sessionId"
            element={
              <ProtectedRoute>
                <Layout>
                  <RevisionPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Core Features */}
          <Route
            path="/avatar"
            element={
              <ProtectedRoute>
                <Layout>
                  <AvatarPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/feynman"
            element={
              <ProtectedRoute>
                <Layout>
                  <FeynmanEnginePage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/story-learning"
            element={
              <ProtectedRoute>
                <Layout>
                  <StoryLearningPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/mistake-autopsy"
            element={
              <ProtectedRoute>
                <Layout>
                  <MistakeAutopsyPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Admin routes */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute requireAdmin>
                <Layout>
                  <AdminHomePage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/questions"
            element={
              <ProtectedRoute requireAdmin>
                <Layout>
                  <ManageQuestionsPage />
                </Layout>
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/users"
            element={
              <ProtectedRoute requireAdmin>
                <Layout>
                  <ManageUsersPage />
                </Layout>
              </ProtectedRoute>
            }
          />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;
