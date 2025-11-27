<script lang="ts">
  // 从父组件接收的属性
  let { headers, list, prevContent, }: { headers: Array<string>, list: Array<any> , prevContent: string} = $props();

  const tipMap = new Map([
    ['酒店预定', '入住城市修改为三亚'],
    ['机票预定', '目的地修改为三亚'],
    ['请假申请', '原因修改为私人事务'],
    ['日程会议', '标题修改为突发事故的处理'],
  ]);

  function getTip(isSingle: boolean) {
    for (let [key, value] of tipMap) {
      if (prevContent.indexOf(key)>=0) {
        return `把${isSingle ? '' : '第一条记录的'}${value}`;
      }
    }
    return '';
  }

</script>

<div class="table">
  <div class="content">
    <ul class="row header">
      <!-- 表头 -->
      <li class="number">序号</li>
      {#each headers as header}
        <li class={header === 'id' ? 'hide' : ''}>{header}</li>
      {/each}
    </ul>
    {#if list.length}
      {#each list as record, index}
        <ul class={index === list.length -1 ? 'row last': 'row'}>
          <li class="number">{index + 1}</li>
          {#each record as property, index}
            <li class={index === 0 ? 'hide' : ''}>{property || '-'}</li>
          {/each}
        </ul>
      {/each}
      <span class="tip">可以对上面的记录进行对话编辑和删除功能，举例：{getTip(list.length === 1)}</span>
    {:else}
      <ul class="row last center">
        <li>-</li>
      </ul>
    {/if}
  </div>

</div>

<style lang="scss">
  .table {
    padding: 0;
    margin: 0;
    overflow-x: scroll;

    .content{
      min-width: 520px;
    }

    .tip{
      font-size: 12px;
      color: #666;
    }
  }
  .table >.content > ul{
    flex: 1;
    box-sizing: border-box;
    display: flex;
    flex-direction: row;

    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  .table >.content > ul > li {
    flex: 1;
    padding: 4px;
    border-top: 1px solid #ddd;
    border-left: 1px solid #ddd;
    box-sizing: border-box;

    &.number{
      flex: none;
      width: 60px;
    }

    &.hide{
      display: none;
    }

    &:last-child{
      border-right: 1px solid #ddd;
    }
  }
  .table >.content > .last {
    border-bottom: 1px solid #ddd;
  }
  .table >.content > .center {
    text-align: center;
  }

  .table .header {
    font-weight: bold;
    background: #f5f5f5;
  }
</style>