import React, { useState, useEffect } from 'react';
import { useQuery } from './convex/_generated';
import { CalendarSummary, CalendarView } from './Calendar';
import './App.css';
import './Calendar.css';

// Types
interface Agent {
  _id: string;
  name: string;
  role: string;
  status: 'active' | 'idle' | 'blocked' | 'offline';
  avatar?: string;
  lastActive: number;
  currentTask?: Task;
  taskCount: number;
}

interface Task {
  _id: string;
  title: string;
  description?: string;
  status: 'inbox' | 'assigned' | 'in_progress' | 'review' | 'done' | 'blocked';
  priority: 'high' | 'medium' | 'low';
  assigneeId?: string;
  assignee?: Agent;
  handoffTo?: string;
  handoffToAgent?: Agent;
  createdAt: number;
  updatedAt: number;
  progress?: number;
  tags: string[];
}

interface Activity {
  _id: string;
  type: string;
  agent?: Agent;
  task?: Task;
  message: string;
  timestamp: number;
}

function App() {
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [view, setView] = useState<'board' | 'agents' | 'activity' | 'calendar'>('calendar');
  const [selectedSite, setSelectedSite] = useState<string | undefined>();

  // Real Convex queries
  const tasks = useQuery("tasks/getTasks", {}) ?? [];
  const agents = useQuery("agents/getAgents", {}) ?? [];
  const activities = useQuery("activities/getActivities", {}) ?? [];

  const renderTaskBoard = () => {
    const columns = [
      { status: 'inbox', title: '📥 Inbox', color: '#e0e0e0' },
      { status: 'assigned', title: '📋 Assigned', color: '#fff3cd' },
      { status: 'in_progress', title: '🔄 In Progress', color: '#cfe2ff' },
      { status: 'review', title: '👀 Review', color: '#e7cff5' },
      { status: 'done', title: '✅ Done', color: '#d1e7dd' },
      { status: 'blocked', title: '🚫 Blocked', color: '#f8d7da' },
    ];

    return (
      <div className="task-board">
        {columns.map((column) => (
          <div key={column.status} className="task-column" style={{ backgroundColor: column.color }}>
            <h3>{column.title}</h3>
            <div className="task-list">
              {tasks
                .filter((task) => task.status === column.status)
                .map((task) => (
                  <div
                    key={task._id}
                    className="task-card"
                    onClick={() => setSelectedTask(task)}
                    style={{ borderLeft: task.priority === 'high' ? '4px solid #dc3545' : '4px solid #6c757d' }}
                  >
                    <div className="task-header">
                      <span className="task-title">{task.title}</span>
                      <span className={`priority priority-${task.priority}`}>{task.priority}</span>
                    </div>
                    {task.assignee && (
                      <div className="task-assignee">
                        {agents.find((a) => a._id === task.assignee)?.avatar}{' '}
                        {agents.find((a) => a._id === task.assignee)?.name}
                      </div>
                    )}
                    {task.progress !== undefined && (
                      <div className="task-progress">
                        <div className="progress-bar">
                          <div className="progress-fill" style={{ width: `${task.progress}%` }}></div>
                        </div>
                        <span className="progress-text">{task.progress}%</span>
                      </div>
                    )}
                    {task.handoffTo && (
                      <div className="task-handoff">
                        → {agents.find((a) => a._id === task.handoffTo)?.name}
                      </div>
                    )}
                    <div className="task-tags">
                      {task.tags.map((tag) => (
                        <span key={tag} className="tag">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderAgents = () => {
    return (
      <div className="agents-grid">
        <h2>👥 Agents</h2>
        <div className="agents-list">
          {agents.map((agent) => (
            <div key={agent._id} className="agent-card">
              <div className="agent-header">
                <span className="agent-avatar">{agent.avatar}</span>
                <div className="agent-info">
                  <h3>{agent.name}</h3>
                  <p className="agent-role">{agent.role}</p>
                </div>
                <span className={`agent-status status-${agent.status}`}>
                  {agent.status}
                </span>
              </div>
              <div className="agent-stats">
                <span>Tasks: {agent.taskCount}</span>
                <span>Last active: {Math.floor((Date.now() - agent.lastActive) / 60000)}m ago</span>
              </div>
              {agent.currentTask && (
                <div className="agent-current-task">
                  <strong>Working on:</strong> {agent.currentTask.title}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderActivity = () => {
    return (
      <div className="activity-feed">
        <h2>📊 Activity Feed</h2>
        <div className="activity-list">
          {activities.map((activity) => (
            <div key={activity._id} className="activity-item">
              <span className="activity-icon">
                {activity.type === 'task_created' && '➕'}
                {activity.type === 'task_assigned' && '👤'}
                {activity.type === 'task_updated' && '✏️'}
                {activity.type === 'task_completed' && '✅'}
                {activity.type === 'task_handoff' && '↪️'}
              </span>
              <div className="activity-content">
                <p>{activity.message}</p>
                <span className="activity-time">
                  {activity.agent && activity.agent.avatar} @{activity.agent.name} • {' '}
                  {new Date(activity.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderTaskDetail = () => {
    if (!selectedTask) return null;

    return (
      <div className="task-detail-modal" onClick={() => setSelectedTask(null)}>
        <div className="task-detail-content" onClick={(e) => e.stopPropagation()}>
          <button className="close-button" onClick={() => setSelectedTask(null)}>
            ×
          </button>
          <h2>{selectedTask.title}</h2>
          <div className="task-meta">
            <span className={`priority priority-${selectedTask.priority}`}>{selectedTask.priority} priority</span>
            <span className={`status status-${selectedTask.status}`}>{selectedTask.status}</span>
          </div>
          {selectedTask.description && <p className="task-description">{selectedTask.description}</p>}
          <div className="task-details-grid">
            <div>
              <strong>Assignee:</strong>{' '}
              {selectedTask.assignee
                ? `${agents.find((a) => a._id === selectedTask.assignee)?.avatar} ${
                    agents.find((a) => a._id === selectedTask.assignee)?.name
                  }`
                : 'Unassigned'}
            </div>
            <div>
              <strong>Created:</strong> {new Date(selectedTask.createdAt).toLocaleString()}
            </div>
            <div>
              <strong>Updated:</strong> {new Date(selectedTask.updatedAt).toLocaleString()}
            </div>
            {selectedTask.handoffTo && (
              <div>
                <strong>Handoff to:</strong>{' '}
                {agents.find((a) => a._id === selectedTask.handoffTo)?.name}
              </div>
            )}
          </div>
          {selectedTask.progress !== undefined && (
            <div className="task-progress-large">
              <strong>Progress:</strong> {selectedTask.progress}%
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${selectedTask.progress}%` }}></div>
              </div>
            </div>
          )}
          <div className="task-tags">
            {selectedTask.tags.map((tag) => (
              <span key={tag} className="tag">
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎛️ Mission Control</h1>
        <nav className="app-nav">
          <button className={view === 'calendar' ? 'active' : ''} onClick={() => setView('calendar')}>
            📅 Calendar
          </button>
          <button className={view === 'board' ? 'active' : ''} onClick={() => setView('board')}>
            📋 Board
          </button>
          <button className={view === 'agents' ? 'active' : ''} onClick={() => setView('agents')}>
            👥 Agents
          </button>
          <button className={view === 'activity' ? 'active' : ''} onClick={() => setView('activity')}>
            📊 Activity
          </button>
        </nav>
      </header>

      <main className="app-main">
        {view === 'calendar' && (
          <div className="calendar-container">
            {selectedSite ? (
              <>
                <button onClick={() => setSelectedSite(undefined)} className="back-button">
                  ← Back to Summary
                </button>
                <CalendarView site={selectedSite} />
              </>
            ) : (
              <CalendarSummary onSelectSite={setSelectedSite} />
            )}
          </div>
        )}
        {view === 'board' && renderTaskBoard()}
        {view === 'agents' && renderAgents()}
        {view === 'activity' && renderActivity()}
      </main>

      {renderTaskDetail()}
    </div>
  );
}

export default App;
