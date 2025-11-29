import type {Message} from "../types/chat";
import {ModelTypes} from "../../constants";
import type {ModelType, TaskExtra} from "../types";

export const chatMessageState: {
  messages: Message[],
  task_type: string,
  model_type: ModelType,
  model: {
    text: {
      query: string,
      task_extra: TaskExtra,
    },
    image: {
      query: string,
      task_extra: TaskExtra,
    },
    video: {
      query: string,
      task_extra: TaskExtra,
    },
  }
} = $state({
  messages: [],
  task_type: '',
  model_type: ModelTypes.Text.value,
  model: {
    text: {
      query: '',
      task_extra: {
        images: []
      },
    },
    image: {
      query: '',
      task_extra: {
        style: '',
        size: '',
        ratio: '',
        n: 0,
        images: []
      },
    },
    video: {
      query: '',
      task_extra: {
        images: [],
        duration: 5,
        size: '',
      },
    },
  }
});