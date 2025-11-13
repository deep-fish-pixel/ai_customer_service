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
    if (Number.isInteger(recent.task_status)) {
      if (isInRecentTask && recent.task_status !== 2) {
        recents.push(recent);
      }
      else if (recent.task_status === 2) {
        const content = getSendMessageData(recent.content);

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
 * 接收消息，对特殊消息的处理，把json字符串进行转换为对象，方便展示
 * @param content
 */
export function getReceiveMessageData(content: string){
  const list = content && content.split(JsonSeperatorRegex.TYPE_LIST) || [];

  return list.map(str => {
    return str.match(/^\[\[/) ? JSON.parse(str) : str;
  });
}


/**
 * 发送消息，对特殊消息的处理，把json字符串进行过滤，只保留列表的id
 * @param content
 */
export function getSendMessageData(content: string){
  const list = getReceiveMessageData(content);

  if (list.length === 2 && Array.isArray(list[1])) {
    list[1] = list[1][1].map((item: Array<any>) => ({"id": item[0]}));

    return list[0] + JSON.stringify(list[1]);
  }
  return content;
}