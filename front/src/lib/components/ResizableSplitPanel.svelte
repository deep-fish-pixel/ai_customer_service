<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  export let leftWidth = 'calc(100% - 350px)';
  export let rightWidth = '350px';
  export let minLeftWidth = '300px';
  export let minRightWidth = '250px';

  let container: HTMLElement;
  let resizer: HTMLElement;
  let isDragging = false;

  const startDrag = (e: MouseEvent) => {
    isDragging = true;
    document.addEventListener('mousemove', handleDrag);
    document.addEventListener('mouseup', stopDrag);
    e.preventDefault();
  };

  const handleDrag = (e: MouseEvent) => {
    if (!isDragging || !container) return;

    const containerRect = container.getBoundingClientRect();
    const newLeftWidth = e.clientX - containerRect.left;
    const containerWidth = containerRect.width;
    const newRightWidth = containerWidth - newLeftWidth;

    if (newLeftWidth >= parseInt(minLeftWidth) && newRightWidth >= parseInt(minRightWidth)) {
      leftWidth = `${newLeftWidth}px`;
      rightWidth = `${newRightWidth}px`;
    }
  };

  const stopDrag = () => {
    isDragging = false;
    document.removeEventListener('mousemove', handleDrag);
    document.removeEventListener('mouseup', stopDrag);
  };

  onDestroy(() => {
    document.removeEventListener('mousemove', handleDrag);
    document.removeEventListener('mouseup', stopDrag);
  });
</script>

<div class="split-container" bind:this={container}>
  <div class="left-panel" style="width: {leftWidth}">
    <slot name="left" />
  </div>
  <div 
    class="resizer" 
    bind:this={resizer}
    on:mousedown={startDrag}
    class:dragging={isDragging}
  />
  <div class="right-panel" style="width: {rightWidth}">
    <slot name="right" />
  </div>
</div>

<style lang="scss">
  .split-container {
    display: flex;
    height: 100%;
    width: 100%;
    position: relative;
  }

  .left-panel {
    height: 100%;
    overflow: hidden;
  }

  .right-panel {
    height: 100%;
    overflow: hidden;
  }

  .resizer {
    width: 4px;
    cursor: col-resize;
    background-color: #e0e0e0;
    transition: background-color 0.2s;

    &:hover {
      background-color: #90caf9;
    }

    &.dragging {
      background-color: #2196f3;
      opacity: 0.8;
    }
  }
</style>