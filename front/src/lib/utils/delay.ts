/**
 * 延迟指定时间后执行回调函数
 * @param ms - 延迟时间(毫秒)
 * @param callback - 可选的回调函数，延迟后执行
 * @returns 包含回调函数返回值的Promise
 */
export function delay<T = void>(ms: number, callback?: () => T | Promise<T>): Promise<T> {
  return new Promise((resolve) => {
    setTimeout(async () => {
      if (callback) {
        const result = await callback();
        resolve(result);
      } else {
        resolve(undefined as unknown as T);
      }
    }, ms);
  });
}