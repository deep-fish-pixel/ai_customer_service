<script lang="ts">
  import Button from '@smui/button';
  import {showToast} from "../../../../utils/toast";
  import {getUserId} from "../../../../state/userState.svelte";
  import PlusIcon from "../../../../icons/PlusIcon.svelte";
  import {chatMessageState} from "../../../../state/chatMessages.svelte";

  initImages();

  function initImages() {
    // 初始化
    if(!chatMessageState.model[chatMessageState.model_type].task_extra.images){
      chatMessageState.model[chatMessageState.model_type].task_extra.images = [];
    }
  }

  // 图片输入处理
  const handleFileInputChange = async (e: Event) => {
    const target = e.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      const file = target.files[0]
      // 限制图片10M内
      if (file.size > 1024 * 1024 * 10) {
        showToast("图片大小不能超过10M");
        return;
      }
      try {
        // 创建FileReader对象
        const reader = new FileReader();
        reader.onload = function(loadEvent) {
          // 获取Base64编码的字符串
          const imageSrc = loadEvent?.target?.result as string;
          initImages();
          if (chatMessageState.model[chatMessageState.model_type].task_extra.images) {
            chatMessageState.model[chatMessageState.model_type].task_extra.images.push(imageSrc);
          }
        };
        reader.readAsDataURL(file);
      } catch (err: any) {
        showToast("上传图片失败：" + err.message);
      }

      // 重置input以便可以再次上传相同的图片
      target.value = '';
    }
  };

  const removeHandle = (index: number) => {
    chatMessageState.model[chatMessageState.model_type].task_extra.images && chatMessageState.model[chatMessageState.model_type].task_extra.images.splice(index, 1);
  }
</script>

<div class="image-uploader">
  <!-- 上传图片区域 -->
  {#each chatMessageState.model[chatMessageState.model_type].task_extra.images as image, index}
    <div class="upload-area">
      <div class="image-container">
        <img src={image}/>
      </div>
      <div class="remove" onclick={() => removeHandle(index)}>-</div>
    </div>
  {/each}
  <div class="upload-area">
    <div class="file-upload">
      <input 
        type="file" 
        id="file-input"
        class="file-input"
        accept=".jpg,.jpeg,.png,.bmp,.webp,.tiff"
        onchange={handleFileInputChange}
      />
      <Button
        class="file-button"
        variant="raised"
        color="primary"
        disabled={!getUserId()}
      >
        <div class="upload-text">
          <PlusIcon />
          <p>添加</p>
        </div>
      </Button>
    </div>
  </div>
</div>

<style lang="scss">
  .image-uploader {
    height: 72px;
    padding: 6px 0;
    display: flex;
    flex-direction: row;

    .upload-area {
      width: 62px;
      height: 72px;
      margin-left: 8px;
      position: relative;

      &:hover{
        .remove{
          display: block;
        }
      }

      .image-container{
        width: 62px;
        height: 72px;
        overflow: hidden;
        position: relative;

        img{
          width: 100%;
          height: 100%;
          object-fit: cover;
          border-radius: 4px;
        }
      }

      .remove{
        width: 14px;
        height: 14px;
        font-size: 16px;
        color: #fff;
        background: #000;
        border-radius: 14px;
        position: absolute;
        top: -5px;
        right: -5px;
        z-index: 1;
        line-height: 11px;
        text-align: center;
        cursor: pointer;
        display: none;
      }
    }

    .file-upload{
      position: relative;
      height: 100%;

      .file-input {
        opacity: 0;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        cursor: pointer;
      }

      :global(.file-button){
        width: 100%;
        height: 100%;
        background-color: #fff;
        box-shadow: none;
        border: 1px solid #eee;
        border-radius: 4px;
      }
    }

    .upload-text{
      color: rgb(102, 102, 102);
      p{
        font-size: 12px;
        padding: 0;
        margin: 0;
      }
    }
  }

  .section-title {
    margin-bottom: 16px;
    color: rgba(0, 0, 0, 0.87);
  }

  .empty-state {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(0, 0, 0, 0.6);
  }


  :global(.MuiListItem-root) {
    border-radius: 8px;
    margin-bottom: 8px;
    transition: background-color 0.2s;

    &:hover {
      background-color: rgba(0, 0, 0, 0.04);
    }
  }

  .document-tab{
    :global(.mdc-deprecated-list-item__secondary-text){
      font-size: 12px;
    }
    :global(.file-list) {
      flex: 1;
      overflow-y: auto;
      padding: 0;
    }
    :global(.file-item){
      padding: 0;
      margin-bottom: 10px;
    }
    :global(.material-icons){
      width: 60px;
      text-align: right;
      font-size: 14px;
      color: var(--mdc-text-button-label-text-color, var(--mdc-theme-primary, #6200ee));
      cursor: pointer;
    }
  }
</style>