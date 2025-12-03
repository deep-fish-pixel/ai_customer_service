import type {Message} from "../types/chat";
import {JsonSeperatorRegex, JsonSeperatorRegexJoinings, RobotPrologue} from "../../constants";

/**
 * 获取最近消息列表
 * @param messages
 * @param size
 */
export function getRecentMessages(messages: Message[], size: number) {
  const recents: Message[] = [];
  const lastMessage = messages[messages.length - 1];
  let index = Math.max(messages.length, 0);
  let isInRecentTask = lastMessage.task_status === 1;

  while(index && size) {
    index--;
    size--;
    const recent = messages[index];

    // 已完成的跳出
    if (Number.isInteger(recent.task_status) && recent.task_status !== -1) {
      if (isInRecentTask && recent.task_status !== 2) {
        recents.push(recent);
      }
      else if (recent.task_status === 2) {
        const content = getSendMessageData(recent);

        recents.push({
          ...recent,
          content,
        });
        isInRecentTask = false;
      }
    } else {
      recents.push(recent);
    }
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

/**
 * 发送消息，对特殊消息的处理，把json字符串进行过滤，只保留列表的id
 * @param message
 */
export function getSendMessageData(message: Message){
  if (message.data_type === 'table') {
    return message.content + JSON.stringify(message.data_value[1].map((item: any) => ({id: item[0]})));
  }
  return message.content;
}