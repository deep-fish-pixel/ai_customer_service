import type {Message} from "../types/chat";

export const chatMessageState: {
  messages: Message[],
  query: string,
  task_type: string,
  task_extra: any,
} = $state({
  messages: [],
  query: '',
  task_type: '',
  task_extra: {
    style: '',
    size: '',
    n: 0,
  },
});