<script lang="ts">
  import ViewVideo from "./ViewVideo.svelte";

  let { list, taskExtra, scrollToBottom}: { list: Array<any>, taskExtra: any, scrollToBottom:() => void} = $props();
  /*
  {"task_id":"09d6a5ff-c192-4cbd-9732-c1518f300dac","task_status":"PENDING","results":[]}
  */
  const ratio = taskExtra && taskExtra.ratio || "1:1";

</script>

<div class={`images-container images-container_${list.length}`}>
  <ul class="images">
    {#each list as task, index(task.task_id || index)}
      <ViewVideo data={task} ratio={ratio} scrollToBottom={scrollToBottom}/>
    {/each}
  </ul>
</div>

<style lang="scss">
  .images-container{
    overflow: hidden;
    overflow-x: scroll;
  }
  .images{
    display: flex;
    flex-direction: row;
    list-style: none;
    padding: 0;
    margin: 2px 0 0 0;

    :global(.image-container){
      &:last-child{
        margin-right: 0;
      }
    }
  }

  .images-container_2{
    .images{
      min-width: 480px;
    }
  }

  .images-container_3{
    .images{
      min-width: 720px;
    }
  }

</style>