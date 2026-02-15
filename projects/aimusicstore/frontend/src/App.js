import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TrendingPage from './pages/TrendingPage';
import Top50Page from './pages/Top50Page';
import SongDetailPage from './pages/SongDetailPage';
import ToolDetailPage from './pages/ToolDetailPage';
import ComingSoonPage from './pages/ComingSoonPage';
function App() {
    return (_jsx(BrowserRouter, { children: _jsxs(Routes, { children: [_jsx(Route, { path: "/", element: _jsx(HomePage, {}) }), _jsx(Route, { path: "/trending", element: _jsx(TrendingPage, {}) }), _jsx(Route, { path: "/top", element: _jsx(Top50Page, {}) }), _jsx(Route, { path: "/songs/:id", element: _jsx(SongDetailPage, {}) }), _jsx(Route, { path: "/tools/:id", element: _jsx(ToolDetailPage, {}) }), _jsx(Route, { path: "/waitlist", element: _jsx(ComingSoonPage, {}) })] }) }));
}
export default App;
