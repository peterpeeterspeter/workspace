import React, { useState, useEffect } from 'react';
import { useQuery, useMutation } from './convex/_generated';
import './App.css';

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
  const [view, setView] = useState<'board' | 'agents' | 'activity'>('board');

  // Real Convex queries
  const tasks = useQuery("tasks/getTasks", {}) ?? [];
  const agents = useQuery("agents/getAgents", {}) ?? [];
  const activities = useQuery("activities/getActivities", {}) ?? [];
