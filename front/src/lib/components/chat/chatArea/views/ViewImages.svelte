<script lang="ts">
  import ViewImage from "./ViewImage.svelte";

  let { list, taskExtra}: { list: Array<any>, taskExtra: any} = $props();
  /*
  {"task_id":"09d6a5ff-c192-4cbd-9732-c1518f300dac","task_status":"PENDING","results":[]}
  */
  const size = taskExtra && taskExtra.size && taskExtra.size.split("*") || ["1328", "1328"];
  const ratio = taskExtra && taskExtra.ratio || "1:1";

</script>

<ul class="image-list">
  {#each list as task, index(task.task_id || index)}
    <ViewImage data={task} ratio={ratio}/>
  {/each}
</ul>

<style lang="scss">
.image-list{
  display: flex;
  flex-direction: row;
  list-style: none;
  padding: 0;
  margin: 8px 0 0 0;
}
</style>