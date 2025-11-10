<script lang="ts">
  // 从父组件接收的属性
  let { headers, list, }: { headers: Array<string>, list: Array<any> } = $props();

</script>

<div class="table">
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
  {:else}
    <ul class="row last center">
      <li>-</li>
    </ul>
  {/if}

</div>

<style lang="scss">
  .table {
    min-width: 520px;
    padding: 0;
    margin: 0;
  }
  .table > ul{
    flex: 1;
    box-sizing: border-box;
    display: flex;
    flex-direction: row;

    list-style-type: none;
    margin: 0;
    padding: 0;
  }
  .table > ul > li {
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
  .table > .last {
    border-bottom: 1px solid #ddd;
  }
  .table > .center {
    text-align: center;
  }

  .table .header {
    font-weight: bold;
    background: #f5f5f5;
  }
</style>