import { create } from 'zustand';

const URL = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}/api`
  : 'http://localhost:8000/api';

type Todo = {
  id: number;
<<<<<<< HEAD
  title: string;
  completed: boolean;
};

type CreateTodo = {
  title: string;
};

type TodoStore = {
  todos: Todo[];
  fetchTodos: () => void;
  addTodo: (todo: CreateTodo) => void;
  updateTodo: (updatedTodo: Todo) => void;
  deleteTodo: (id: number) => void;
};

const URL = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}/api`
  : "http://localhost:3000/api";

export const useStore = create<TodoStore>((set) => ({
  todos: [],
  fetchTodos: async () => {
=======
  prompt: string;
  reply: string;
};

type CreateChat = {
  prompt: string;
};

type ChatStore = {
  chats: Chat[];
  fetchChats: () => Promise<void>;
  addChat: (chat: CreateChat) => Promise<void>;
};

export const useStore = create<ChatStore>((set, get) => ({
  chats: [],
  fetchChats: async () => {
>>>>>>> d7a1d41926f4c65238a6481e61978ee1d030278e
    try {
      const response = await fetch(`${URL}/todos`);
      const todos = await response.json();
      set({ todos });
    } catch (error) {
<<<<<<< HEAD
      console.error("Error fetching todos:", error);
    }
  },
  addTodo: async (todo) => {
    try {
      const response = await fetch(`${URL}/todos`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(todo),
      });
      const createdTodo = await response.json();
      set((state) => ({ todos: [...state.todos, createdTodo] }));
    } catch (error) {
      console.error("Error creating todo:", error);
    }
  },
  updateTodo: async (updatedTodo) => {
    try {
      const response = await fetch(`${URL}/todos/${updatedTodo.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedTodo),
      });
      const updatedItem = await response.json();
      set((state) => ({
        todos: state.todos.map((todo) =>
          todo.id === updatedItem.id ? updatedItem : todo
        ),
      }));
    } catch (error) {
      console.error("Error updating todo:", error);
    }
  },
  deleteTodo: async (id) => {
    try {
      await fetch(`${URL}/todos/${id}`, {
        method: "DELETE",
      });
      set((state) => ({
        todos: state.todos.filter((todo) => todo.id !== id),
      }));
    } catch (error) {
      console.error("Error deleting todo:", error);
    }
  },
=======
      console.error('Error fetching chats:', error);
    }
  },
// In store.ts
addChat: async (chat: CreateChat) => {
  try {
    const id = get().chats.length + 1; // Store the ID here to use later
    set((state) => ({ chats: [...state.chats, { ...chat, id: id, reply: '' }] }));
    
    const eventSource = new EventSource(`${URL}/stream?prompt=${encodeURIComponent(chat.prompt)}`);
    
    eventSource.onmessage = (event) => {
      const data = event.data;
      set((state) => {
        const chats = state.chats.map((c) => {
          if (c.id === id) {
            return { ...c, reply: c.reply + data };
          }
          return c;
        });
        return { chats };
      });
    };

    eventSource.addEventListener('end-of-stream', () => {
      console.log('Chat stream ended normally.');
      eventSource.close();
      set((state) => {
        const chats = state.chats.map((c) => {
          if (c.id === id) {
            return { ...c, reply: c.reply.trim() }; // Trim any possible trailing newlines
          }
          return c;
        });
        return { chats };
      });
    });

    eventSource.onerror = (error) => {
      if (eventSource.readyState === EventSource.CLOSED) {
        console.log('Chat stream ended normally.');
      } else {
        console.error('Error with the chat stream:', error);
      }
      eventSource.close();
    };

  } catch (error) {
    console.error('Error adding chat:', error);
  }
},
>>>>>>> d7a1d41926f4c65238a6481e61978ee1d030278e
}));
