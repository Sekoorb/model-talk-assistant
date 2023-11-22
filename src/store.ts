import { create } from "zustand";

type Chat = {
  id: number;
  prompt: string;
  reply: string;
  helpful: boolean;
};

type CreateChat = {
  prompt: string;
  reply: string;
};

type ChatStore = {
  chats: Chat[];
  fetchChats: () => void;
  addChat: (chat: CreateChat) => void;
  updateChat: (updatedChat: Chat) => void;
  deleteChat: (id: number) => void;
};
                                                                                                                                                                                                                                                                                                                 
const URL = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}/api`
  : "http://localhost:3000/api";

export const useStore = create<ChatStore>((set) => ({
  chats: [],
  fetchChats: async () => {
    try {
      const response = await fetch(`${URL}/chats`);
      const chats = await response.json();
      set({ chats });
    } catch (error) {
      console.error("Error fetching chats:", error);
    }
  },
  addChat: async (chat) => {
    try {
      const response = await fetch(`${URL}/chats`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(chat),
      });
      const createdChat = await response.json();
      set((state) => ({ chats: [...state.chats, createdChat] }));
    } catch (error) {
      console.error("Error creating chat:", error);
    }
  },
  updateChat: async (updatedChat) => {
    try {
      const response = await fetch(`${URL}/chats/${updatedChat.id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedChat),
      });
      const updatedItem = await response.json();
      set((state) => ({
        chats: state.chats.map((chat) =>
          chat.id === updatedItem.id ? updatedItem : chat
        ),
      }));
    } catch (error) {
      console.error("Error updating chat:", error);
    }
  },
  deleteChat: async (id) => {
    try {
      await fetch(`${URL}/chats/${id}`, {
        method: "DELETE",
      });
      set((state) => ({
        chats: state.chats.filter((chat) => chat.id !== id),
      }));
    } catch (error) {
      console.error("Error deleting chat:", error);
    }
  },
}));
