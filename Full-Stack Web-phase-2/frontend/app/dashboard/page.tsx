'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { taskAPI } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { PlusIcon, TrashIcon, PencilIcon } from 'lucide-react';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: number;
}

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [editingTitle, setEditingTitle] = useState('');
  const [editingDescription, setEditingDescription] = useState('');

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user]);

  const fetchTasks = async () => {
    if (!user) return;
    
    try {
      setLoading(true);
      const tasksData = await taskAPI.getUserTasks(user.id);
      setTasks(tasksData);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newTaskTitle.trim() || !user) return;
    
    try {
      const newTask = await taskAPI.createTask(user.id, newTaskTitle, newTaskDescription);
      setTasks([newTask, ...tasks]);
      setNewTaskTitle('');
      setNewTaskDescription('');
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (!user) return;
    
    try {
      await taskAPI.deleteTask(user.id, taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const handleToggleTask = async (taskId: number, completed: boolean) => {
    if (!user) return;
    
    try {
      const updatedTask = await taskAPI.toggleTaskCompletion(user.id, taskId, !completed);
      setTasks(tasks.map(task => 
        task.id === taskId ? updatedTask : task
      ));
    } catch (error) {
      console.error('Failed to toggle task:', error);
    }
  };

  const startEditingTask = (task: Task) => {
    setEditingTask(task);
    setEditingTitle(task.title);
    setEditingDescription(task.description || '');
  };

  const handleUpdateTask = async () => {
    if (!editingTask || !user) return;
    
    try {
      const updatedTask = await taskAPI.updateTask(user.id, editingTask.id, {
        title: editingTitle,
        description: editingDescription || undefined,
        completed: editingTask.completed,
      });
      
      setTasks(tasks.map(task => 
        task.id === editingTask.id ? updatedTask : task
      ));
      
      setEditingTask(null);
      setEditingTitle('');
      setEditingDescription('');
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen p-8">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold">Loading your tasks...</h1>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(3)].map((_, i) => (
              <Card key={i}>
                <CardHeader>
                  <CardTitle><div className="h-6 bg-gray-200 rounded w-3/4"></div></CardTitle>
                  <CardDescription><div className="h-4 bg-gray-200 rounded w-1/2"></div></CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="h-4 bg-gray-200 rounded"></div>
                    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="flex justify-between items-center mb-8 p-4 bg-white rounded-lg shadow-sm">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold">Task Dashboard</h1>
            <p className="text-gray-600">Welcome back, {user?.email}</p>
          </div>
          <Button variant="outline" onClick={logout}>Logout</Button>
        </header>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Total Tasks</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{tasks.length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Completed</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{tasks.filter(t => t.completed).length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Pending</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{tasks.filter(t => !t.completed).length}</div>
            </CardContent>
          </Card>
        </div>

        {/* Add Task Form */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Add New Task</CardTitle>
            <CardDescription>Create a new task to stay organized</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreateTask} className="flex flex-col sm:flex-row gap-4">
              <div className="flex-grow">
                <Label htmlFor="task-title">Task Title</Label>
                <Input
                  id="task-title"
                  placeholder="What needs to be done?"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  required
                />
              </div>
              <Button type="submit" className="self-end">
                <PlusIcon className="mr-2 h-4 w-4" /> Add Task
              </Button>
            </form>
            <div className="mt-4">
              <Label htmlFor="task-description">Description (optional)</Label>
              <Input
                id="task-description"
                placeholder="Add details..."
                value={newTaskDescription}
                onChange={(e) => setNewTaskDescription(e.target.value)}
              />
            </div>
          </CardContent>
        </Card>

        {/* Tasks List */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Your Tasks</h2>
          
          {tasks.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-gray-500">No tasks yet. Add your first task above!</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tasks.map((task) => (
                <Card key={task.id} className={`transition-all ${task.completed ? 'opacity-70' : ''}`}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div className="flex items-start space-x-2">
                        <Checkbox
                          checked={task.completed}
                          onCheckedChange={() => handleToggleTask(task.id, task.completed)}
                          className="mt-1"
                        />
                        <div>
                          <CardTitle className={`${task.completed ? 'line-through text-gray-500' : ''}`}>
                            {task.title}
                          </CardTitle>
                          <p className="text-sm text-gray-500 mt-1">
                            {formatDate(task.created_at)}
                          </p>
                        </div>
                      </div>
                      <div className="flex space-x-1">
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => startEditingTask(task)}
                            >
                              <PencilIcon className="h-4 w-4" />
                            </Button>
                          </DialogTrigger>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>Edit Task</DialogTitle>
                              <DialogDescription>
                                Update your task details
                              </DialogDescription>
                            </DialogHeader>
                            <div className="space-y-4 py-4">
                              <div>
                                <Label htmlFor="edit-title">Title</Label>
                                <Input
                                  id="edit-title"
                                  value={editingTitle}
                                  onChange={(e) => setEditingTitle(e.target.value)}
                                />
                              </div>
                              <div>
                                <Label htmlFor="edit-description">Description</Label>
                                <Input
                                  id="edit-description"
                                  value={editingDescription}
                                  onChange={(e) => setEditingDescription(e.target.value)}
                                />
                              </div>
                              <div className="flex justify-end space-x-2">
                                <Button 
                                  variant="outline" 
                                  onClick={() => setEditingTask(null)}
                                >
                                  Cancel
                                </Button>
                                <Button 
                                  onClick={handleUpdateTask}
                                >
                                  Save
                                </Button>
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                        
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDeleteTask(task.id)}
                        >
                          <TrashIcon className="h-4 w-4 text-red-500" />
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    {task.description && (
                      <p className="text-gray-700">{task.description}</p>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}