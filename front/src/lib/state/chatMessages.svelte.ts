import type {Message} from "../types/chat";

export const chatMessageState: {
  messages: Message[],
  query: string,
  task_type: string,
  task_extra: {
    style?: string;
    size?: string;
    ratio?: string;
    n?: number;
    images?: string[];
  },
  model_index: number,
} = $state({
  messages: [],
  query: '',
  task_type: '',
  model_index: 0,
  task_extra: {
    style: '',
    size: '',
    ratio: '',
    n: 0,
    images: []
  },
});