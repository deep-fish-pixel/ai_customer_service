import type {Message} from "../types/chat";

export const chatMessageState: {
  messages: Message[]
} = $state({
  messages: []
});