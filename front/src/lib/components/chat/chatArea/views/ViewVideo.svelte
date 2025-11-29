<script lang="ts">
  // 从父组件接收的属性
  import {onMount} from "svelte";
  import {
    ImageRatioTypes,
    RESPONSE_STATUS_FAILED,
    RESPONSE_STATUS_SUCCESS,
    VideoRatioTypes
  } from "../../../../../constants";
  import {getVideoTask} from "../../../../services/mutiModelService";
  import {Exception} from "sass";
  import type {Response} from "../../../../types/request";


  let { data, ratio, scrollToBottom }: { data: {
      task_id?: string;
      task_status: string;
      video_url: string;
      image?: string;
    }; ratio: keyof typeof VideoRatioTypes;  scrollToBottom:() => void} = $props();

  const style = VideoRatioTypes[ratio].style || VideoRatioTypes["1:1"].style;
  const [width, height] = style;
  let lottieContainer: HTMLElement;
  let videoUrl = $state('');
  let animation: any;

  const loadHandle = (event: any) => {
    event.target.classList.add('loaded');
    animation && animation.stop();
    lottieContainer.style.display = 'none';
  };

  onMount(async () => {
    const lottie = window.lottie;
    if (lottie) {
      animation = lottie.loadAnimation({
        container: lottieContainer,
        renderer: 'svg',
        loop: true,
        autoplay: true,
        ratio: 'none',
        // 使用一个公开的波纹 Lottie JSON（可替换为你自己的）
        path: '/lottie_animate.json', // 示例：圆形波纹
        rendererSettings: {
          preserveAspectRatio: "none",
        }
      });
    }

    if (data.task_id && (data.task_status === 'PENDING' || data.task_status === 'RUNNING') && !data.video_url) {
      try{
        const response = await getRequestPromise(getVideoTask, data.task_id);
        if (response.status === RESPONSE_STATUS_SUCCESS) {
          videoUrl = response.data.video_url;
        } else {
          // todo 加载失败
        }
      }catch (e) {
        console.error(e);
      }
    }
  });

  function getRequestPromise(request: any, task_id: string) : Promise<Response<any>>{
    return new Promise((resove, reject) => {
      getLoopRequest(resove, reject, request, task_id);
    })
  }

  function getLoopRequest(resove: any, reject:any, request: any, task_id: string, duration = 3000) {
    request(task_id).then((res: any) => {
      const { process, video_url, params, } = res.data;

      if (process === 'SUCCEEDED') {
        resove({
          status: RESPONSE_STATUS_SUCCESS,
          data: {
            video_url,
            params,
          },
        });
      }
      else if (process === 'FAILED') {
        resove({
          status: RESPONSE_STATUS_FAILED,
          message: "图片生成失败",
          data: null,
        });
      }
      else if (process === 'CANCELED') {
        resove({
          status: RESPONSE_STATUS_FAILED,
          message: "图片生成任务取消",
          data: null,
        });
      }
      else {
        setTimeout(() => getLoopRequest(resove, reject, request, task_id, duration), duration);
      }
    }).catch((e: Exception) => {
      console.log(e);
      reject(e);
    });
  }
</script>

<li class="image-container" style={`width:${width ? width + 'px' : 'initial' };height:${height ? height + 'px' : 'initial' }`}>
  <div class="lottie-placeholder" bind:this={lottieContainer}></div>
  <video class="image" src={videoUrl} controls onloadeddata={loadHandle}></video>
</li>

<style lang="scss">
  .image-container {
    position: relative;
    border-radius: 4px;
    padding: 0;
    margin: 0 10px 0 0;

    :global(.loaded){
      opacity: 1;
    }
  }
  .lottie-placeholder {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-image: url('data:image/webp;base64,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');
    border-radius: 8px;
  }
  .image {
    width: 100%;
    height: 100%;
    max-width: 400px;
    object-fit: cover;
    opacity: 0;
    transition: opacity 0.4s ease;
    border-radius: 8px;
  }
</style>