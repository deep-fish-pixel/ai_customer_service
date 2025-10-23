/**
 * 日期格式化工具
 * 提供日期格式化和当前日期获取功能
 */

/**
 * 格式化日期为指定格式的字符串
 * @param date - 要格式化的日期对象或时间戳
 * @param format - 日期格式字符串，支持的占位符：
 *                 YYYY: 4位年份
 *                 MM: 2位月份(01-12)
 *                 DD: 2位日期(01-31)
 *                 HH: 24小时制小时(00-23)
 *                 mm: 分钟(00-59)
 *                 ss: 秒(00-59)
 * @returns 格式化后的日期字符串
 * @example formatDate(new Date(), 'YYYY-MM-DD HH:mm:ss') => '2023-10-25 14:30:45'
 */
export function formatDate(date: Date | number, format: string): string {
  if (!date) {
      return '-'
  }
  // 处理时间戳情况
  if (typeof date === 'number') {
    date = new Date(date);
  }

  // 确保日期对象有效
  if (!(date instanceof Date) || isNaN(date.getTime())) {
    throw new Error('无效的日期对象或时间戳');
  }

  const year = date.getFullYear();
  const month = date.getMonth() + 1; // 月份从0开始
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = date.getMinutes();
  const seconds = date.getSeconds();

  // 补零函数
  const padZero = (num: number): string => num.toString().padStart(2, '0');

  // 替换格式字符串中的占位符
  return format
    .replace('YYYY', year.toString())
    .replace('MM', padZero(month))
    .replace('DD', padZero(day))
    .replace('HH', padZero(hours))
    .replace('mm', padZero(minutes))
    .replace('ss', padZero(seconds));
}

/**
 * 获取当前日期的格式化字符串
 * @param format - 日期格式字符串，同formatDate方法
 * @returns 当前日期的格式化字符串
 */
export function getCurrentDate(format: string = 'YYYY-MM-DD'): string {
  return formatDate(new Date(), format);
}