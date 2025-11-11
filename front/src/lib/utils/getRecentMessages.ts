import type {Message} from "../types/chat";
import {RobotPrologue} from "../../constants";

/**
 * 获取最近消息列表
 * @param messages
 * @param size
 */
export default function (messages: Message[], size: number) {
  const recents: Message[] = [];
  let index = Math.max(messages.length, 0);

  while(index && size) {
    index--;
    size--;
    const recent = messages[index];

    // 已完成的跳出
    if (recent.task_status === 2) {
      break;
    }

    recents.push(recent);
  }

  if (recents.length === 0) {
    recents.push({
      id: '1',
      content: RobotPrologue,
      sender: 'bot',
      timestamp: new Date()
    })
  }


  return recents.reverse();
}