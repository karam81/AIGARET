<template>
  <v-container fluid class="text-center">
    <div>
      <div id="outer" class="row">

        <!-- 왼쪽 div 영역(div_inner_left) -->
        <div id="div_inner_left" class="col-md-4" style="height: 100px; padding-top: 70px; background-color: transparent; display: flex; justify-content: center; flex-wrap: wrap">

          <!-- 왼쪽 첫 번째 div(div_left_first) : 내 프로필 사진이 보여짐. -->
          <div id="div_inner_left_first" style="width: 400px; height: 300px; background-color: transparent; text-align: center; margin-bottom: 15px">
            <!-- <v-img src="@/assets/ryan.png" width="400px" height="300px"></v-img> -->
            <v-img :src="image" width="400px" height="300px" style=""></v-img>
          </div>

          <!-- 왼쪽 두 번째 div(div_left_second) : 내 정보 변경, 사진 변경, 목표시간 변경 버튼이 있음. -->
          <div id="div_inner_left_second" style="margin-bottom: 15px">
            
            <!-- 1. 비밀번호 변경 다이얼로그 -->
            <v-dialog v-model="dialog_change_password" width="500" persistent>
              <template v-slot:activator="{ on, attrs }">
                <v-btn width="133px" class="mx-1" dark v-bind="attrs" v-on="on" style="background: #53cde2">
                  <v-icon>mdi-account-edit</v-icon>
                </v-btn>
              </template>s

              <v-card>
                <ValidationObserver v-slot="{ invalid }">
                  <v-card-title class="headline justify-center" style="background: #005792">
                    <p class="ma-2" style="color: white; font-family: CookieRun-Bold">비밀번호 변경</p>
                  </v-card-title>

                  <v-card-text>
                    <v-form class="ma-4" ref="form" @submit.prevent>
                      <v-text-field v-model="userInfo.old_password" label="현재 비밀번호" name="password" type="password" required style="font-family: CookieRun-Bold"></v-text-field>

                      <ValidationProvider mode="eager" v-slot="{ errors }" name="NewPassword" vid="confirmation" :rules="{ required: true, min: 4 }">
                        <v-text-field v-model="userInfo.new_password" :error-messages="errors" label="변경할 비밀번호" name="newPassword" type="password" style="font-family: CookieRun-Bold"></v-text-field>
                      </ValidationProvider>

                      <ValidationProvider mode="eager" v-slot="{ errors }" name="NewPasswordConfirm" rules="required|confirmed:confirmation">
                        <v-text-field v-model="userInfo.new_passwordConfirm" :error-messages="errors" label="비밀번호 확인" name="newPasswordConfirm" type="password" style="font-family: CookieRun-Bold" @keypress.enter="changePassword(userInfo); clearForm()"></v-text-field>
                      </ValidationProvider>
                    </v-form>
                  </v-card-text>

                  <v-card-actions>  
                    <div style="width: 100%; margin: 0 10px; text-align: center">
                      <v-btn color="primary" style="margin: 10px 10px; font-family: CookieRun-Bold" @click="changePassword(userInfo); clearForm()" :disabled="invalid" >변경</v-btn>
                      <v-btn color="error" style="margin: 10px 10px font-family: CookieRun-Bold" @click="dialog_change_password = false; clearForm()">취소</v-btn>
                    </div>
                  </v-card-actions>
                </ValidationObserver>
              </v-card>
            </v-dialog>

            <!-- 2. 사진 변경 다이얼로그 -->
            <v-dialog v-model="dialog_change_image" width="500" persistent>
              <template v-slot:activator="{ on, attrs }">
                <v-btn width="133px" class="mx-1" dark v-bind="attrs" v-on="on" @click="videoStart()" style="background: #006cb5">
                  <v-icon>mdi-camera-retake</v-icon>
                </v-btn>
              </template>

              <v-card>
                <v-card-title class="headline justify-center" style="background: #005792">
                  <p class="ma-2" style="color: white; font-family: CookieRun-Bold">사진 변경</p>
                </v-card-title>

                <v-card-text style="padding-bottom: 10px">
                  <div class="my-2" style="display: flex; justify-content: center; align-items: center">
                    <video id="video" width="400" height="300" autoplay muted></video>
                    <canvas id="canvas" width="400" height="300" style="position: absolute"></canvas>
                  </div>

                  <div class="my-2" style="display: flex; justify-content: center;">
                    <v-btn class="mx-2" fab @click="videoPauseAndCapture">
                      <v-icon>mdi-camera</v-icon>
                    </v-btn>
                    <v-btn class="mx-2" fab @click="videoResume">
                      <v-icon>mdi-refresh</v-icon>
                    </v-btn>
                  </div>
                  <v-divider></v-divider>

                  <div class="my-2" style="display: flex; justify-content: center">
                    <v-btn class="mx-2" color="error" @click="changeImage(base64Encoded); cancelChangingPicture()" :disabled="!isCaptured" style="font-family: CookieRun-Bold">변경</v-btn>
                    <v-btn class="mx-2" color="primary" @click="cancelChangingPicture" style="font-family: CookieRun-Bold">취소</v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-dialog>

            <!-- 3. 목표 시간 변경 다이얼로그-->
            <v-dialog v-model="dialog_change_goal_time" width="500" persistent>
              <template v-slot:activator="{ on, attrs }">
                <v-btn width="133px" class="mx-1" dark v-bind="attrs" v-on="on" style="background: #005792">
                  <v-icon>mdi-human-edit</v-icon>
                </v-btn>
              </template>

              <v-card id="slider">
                <v-card-title class="headline justify-center" style="background: #005792">
                  <p class="ma-2" style="color: white; font-family: CookieRun-Bold">목표 시간 변경</p>
                </v-card-title>

                <v-card-text style="padding-bottom: 10px">


                  <div class="my-2" style="display: flex; justify-content: center;">
                    <v-slider
                      v-model="newGoalTime"
                      hint="일주일 목표 시간을 설정해주세요."
                      max="24"
                      min="0"
                      label="일주일 목표 시간(시간)"
                      thumb-label
                      :thumb-size="50"
                      :rules="rules"
                    ></v-slider>
                  </div>

                  <v-divider></v-divider>

                  <div class="my-2" style="display: flex; justify-content: center">
                    <v-btn class="mx-2" color="error" @click="changeGoalTime(newGoalTime); dialog_change_goal_time = false" :disabled="newGoalTime == 0" style="font-family: CookieRun-Bold">변경</v-btn>
                    <v-btn class="mx-2" color="primary" @click="dialog_change_goal_time = false; newGoalTime = 1" style="font-family: CookieRun-Bold">취소</v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </v-dialog>
          </div>

          <!-- 왼쪽 세 번째 div(div_left_third) : 캘린더, 통계 버튼 위치. -->
          <div id="div_left_third" style="width: 90%; text-align: center;">
              <v-btn-toggle v-model="btnIdx" mandatory style="width: 70%; display: inline-block; background: transparent">
                <!-- <v-btn class="facebook" style="width: 100%;">
                    <v-icon color="white">mdi-calendar</v-icon>
                    <span style="font-size: 20px; color: white">캘린더</span>
                </v-btn>
                <v-btn class="facebook" style="width: 100%;">
                  <v-icon color="white">mdi-chart-box</v-icon>
                  <span style="font-size: 20px; color: white">통계</span>
                </v-btn> -->
                <v-btn class="button twitter" style="width: 100%; height: 80px; margin-bottom: 5px">
                  <v-icon color="white" style="font-size: 3vw;">mdi-calendar</v-icon>
                  <p style="padding-top: 8px">캘린더</p>
                </v-btn>
                <v-btn class="button twitter" style="width: 100%; height: 80px">
                  <v-icon color="white" style="font-size: 3vw;">mdi-chart-box</v-icon>
                  <p style="padding-top: 8px">통계</p>
                </v-btn>
              </v-btn-toggle>
          </div>
        </div>

        <!-- 오른쪽 div 영역(div_inner_left) -->
        <div id="div_inner_right" class="col-md-8" style="background-color: transparent;">
          
          <!-- 달성률 영역-->
          <div style="text-align: center">
            <p class="text-md-left font-weight-bold" style="font-size: 2rem; font-family: CookieRun-Bold">&#127919;한 주동안 얼마나 했을까?({{ parseInt($store.state.mypageStore.total_time / 60) }}분 / {{ goal_time * 60 }}분)</p>
            <v-progress-linear id="MY_PROGRESS" center rounded :value="progressValue" height="35" color="#FF0084" style="width: 100%; display: inline-block; font-size: 30px">&#128293;목표 달성까지 {{ 100 - progressValue }}%&#128293;</v-progress-linear>
          </div>

          <!-- 캘린더 OR 통계 영역 -->
          <div id="div_inner_right_first" class="ma-2" style="background: transparent; height: 700.844px">
            <div v-if="btnIdx == 0">
              <p class="text-md-left font-weight-bold" style="font-size: 2rem; font-family: CookieRun-Bold;">&#128198;캘린더(<img src="../../assets/stamp3.png" width="50px" /> : 10분 이상, <img src="../../assets/stamp.png" width="50px" /> : 30분 이상)</p>&emsp;
              <Calendar style="padding-top: 0px"/>
            </div>
            
            <div v-if="btnIdx == 1">
              <p class="text-md-left font-weight-bold" style="font-size: 2rem; font-family: CookieRun-Bold;">&#128200;통계</p>&emsp;
              <!-- <BarChart class="ma-5" style="width: 400px; height: 450px; display: inline-block"/> -->
              <LineChart class="ma-5" style="width: 400px; height: 450px; display: inline-block"/>
              <PieChart class="ma-5" style="width: 400px; height: 450px; display: inline-block"/>
            </div>  
          </div>

          <!-- 2. 각 게임별 일주일 데이터 -->
          <!-- <div id="div_inner_right_second" class="ma-2 pa-1" style="background: yellow;">
            <div>
              <v-btn>손목</v-btn>
              <v-btn>스네이크</v-btn>
              <v-btn>점프</v-btn>
            </div>
            <p class="text-md-left font-weight-bold" style="font-size: 2rem; font-family: CookieRun-Bold;">진행 현황</p>
            <v-progress-circular class="mx-10 my-2" color="green lighten-2" :size="100" :width="15" value="60" style="font-family: CookieRun-Bold">팔</v-progress-circular>
            <v-progress-circular class="mx-10 my-2" color="blue lighten-2" :size="100" :width="15" value="30" style="font-family: CookieRun-Bold">다리</v-progress-circular>
            <v-progress-circular class="mx-10 my-2" color="pink lighten-2" :size="100" :width="15" value="80" style="font-family: CookieRun-Bold">몸</v-progress-circular>
          </div> -->
        </div>
      </div>

      <!-- </v-row> -->
    </div>
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

import $ from 'jquery'
import * as faceapi from 'face-api.js'
import moment from 'moment'

import { extend, ValidationObserver, setInteractionMode, ValidationProvider } from 'vee-validate'
import { required, email, max, min, regex, confirmed } from 'vee-validate/dist/rules'

import BarChart from '@/components/Account/BarChart'
import LineChart from '@/components/Account/LineChart'
import PieChart from '@/components/Account/PieChart'
import Calendar from '@/components/Account/Calendar'

const userStore = 'userStore'
const mypageStore = 'mypageStore'

extend('required', {
  ...required,
  message: '{_field_} 값은 반드시 입력해야 합니다.'
})

extend('confirmed', {
  ...confirmed,
  message: '비밀번호가 같지 않습니다.'
})

extend('min', {
  ...min,
  message: '{_field_} 값은 최소 {length}자리 이상이어야 합니다.'
})

export default {
  components: {
    ValidationObserver,
    ValidationProvider,

    BarChart,
    LineChart,
    PieChart,
    Calendar
  },

  data () {
    return {
      item: 0,
      items: [
        { text: '캘린더', icon: 'mdi-calendar' },
        { text: '통계', icon: 'mdi-chart-box' },
      ],

      dialog_my_info: '',
      dialog_change_password: '',
      dialog_change_image: '',
      dialog_change_goal_time: '',

      video: document.getElementById('video'),
      canvas: document.getElementById('canvas'),
      localStream: '',

      userInfo: {
        old_password: '',
        new_password: '',
        new_passwordConfirm: ''
      },

      videoFlag: false,
      timerId: null,

      isCaptured: false,

      base64Encoded: '',

      newGoalTime: 1,
      rules: [
        v => v != 0 || '최소 1시간 이상으로 설정해주세요.',
      ],

      date: {
        'start_date': '',
        'end_date': ''
      },
      btnIdx: 0
    }
  },

  mounted () {
    let prevSunday = moment().day(0).year() + "-" + ((moment().day(0).month()+1) >= 10 ? (moment().day(0).month()+1) : ('0' + (moment().day(0).month()+1))) + "-" + ((moment().day(0).date()) >= 10 ? (moment().day(0).date()) : ('0' + (moment().day(0).date())))
    let nextSunday = moment().day(7).year() + "-" + ((moment().day(7).month()+1) >= 10 ? (moment().day(7).month()+1) : ('0' + (moment().day(7).month()+1))) + "-" + ((moment().day(7).date()) >= 10 ? (moment().day(7).date()) : ('0' + (moment().day(7).date())))
    
    this.date.start_date = prevSunday
    this.date.end_date = nextSunday

    this.getAchievePercent(this.date).then(() => {
      // console.log("total_time : ", this.$store.state.total_time)
      // console.log("goal_time : ", this.goal_time)
      
      // this.progressValue = (parseInt(this.$store.state.total_time / 3600) / this.goal_time * 100).toFixed(1)
      // console.log('this.progressValue : ', this.progressValue)

      // console.log('this.$store.state.mypageStore.total_time : ', this.$store.state.mypageStore.total_time)
    })
  },

  updated () {
    // console.log('Info.vue updated.')
    // console.log('updated - videoFlag : ', this.videoFlag)

    if (this.videoFlag == true) {
      this.video = document.getElementById('video')
      this.canvas = document.getElementById('canvas')

      // this.faceDetect()
    } else {
      this.video = null
      this.canvas = null
    }
  },

  computed: {
    ...mapGetters(userStore, ['image', 'goal_time']),
    ...mapGetters(mypageStore, ['progressValue']),

    // image() {
    //   return this.$store.state.userInfo.profile_image
    // },

    // goal_time() {
    //   return this.$store.state.userInfo.goal_time
    // },

    // progressValue() {
    //   return this.$store.getters.progressValue
    // }
  },

  methods: {
    ...mapActions(userStore, ['changePassword', 'changeImage', 'changeGoalTime']),
    ...mapActions(mypageStore, ['getAchievePercent']),

    videoStart () {
      this.videoFlag = true

      navigator.getUserMedia(
        { video: {} },
        stream => {
          video.srcObject = stream
          this.localStream = stream
        },
        err => console.error(err)
      )
    },

    videoPauseAndCapture () {
      this.isCaptured = true
      const video = this.video
      const canvas = this.canvas

      $('#video').get(0).pause()
      var ctx = canvas.getContext('2d')

      // if (this.timerId != null) { clearInterval(this.timerId) }
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
      // console.log(canvas.toDataURL())

      const base64Encoded = canvas.toDataURL()
      // console.log(base64Encoded)
      this.base64Encoded = base64Encoded
    },

    videoResume () {
      this.isCaptured = false

      if (this.timerId != null) { clearInterval(this.timerId) }

      $('#video').get(0).play()
    },

    async faceDetect () {
      // console.log('this.video.width', this.video.width)
      // console.log('this.video.height', this.video.height)

      const video = this.video
      const canvas = this.canvas

      const displaySize = { width: video.width, height: video.height }
      faceapi.matchDimensions(canvas, displaySize)

      await faceapi.nets.ssdMobilenetv1.loadFromUri('/models')
      await faceapi.nets.faceLandmark68Net.loadFromUri('/models')
      await faceapi.nets.faceRecognitionNet.loadFromUri('/models')
      await faceapi.nets.faceExpressionNet.loadFromUri('/models')

      this.timerId = setInterval(async () => {
        // console.log('계속 도는 중.')
        const detections = await faceapi.detectAllFaces(video).withFaceLandmarks().withFaceExpressions()
        const resizedDetections = faceapi.resizeResults(detections, displaySize)
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
        faceapi.draw.drawDetections(canvas, resizedDetections)
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
        faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
      }, 100)
    },

    cancelChangingPicture () {
      this.isCaptured = false
      this.localStream.getTracks()[0].stop()
      if (this.timerId != null) { clearInterval(this.timerId) }
      setTimeout(() => {
        this.dialog_change_image = false
      }, 500)

      this.videoFlag = false
    },

    clearForm() {
      this.$refs.form.reset()
    }
  }
}
</script>

<style>
.basil {
  background-color: #fcfeff !important;
}
.basil--text {
  color: #356859 !important;
}

body {
  overflow: hidden
}

#slider {
  overflow-x: hidden
}

.facebook {
    background: #99b6df;
    background: -webkit-gradient(linear, 0 0, 0 bottom, from(#99b6df), to(#638ec8));
    background: -moz-linear-gradient(#99b6df, #638ec8);
    background: linear-gradient(#99b6df, #638ec8);
    border: solid 1px #6d94ce;
    border-bottom: solid 3px #3867ac;
    box-shadow: inset 0 0 0 1px #bbcfeb;
    color: #fff;
    text-shadow: 0 1px 0 #3c61ab; }
    
.facebook:hover {
    background: #638ec8;
    background: -webkit-gradient(linear, 0 0, 0 bottom, from(#638ec8), to(#99b6df));
    background: -moz-linear-gradient(#638ec8, #99b6df);
    background: linear-gradient(#638ec8, #99b6df);
    border: solid 1px #6d94ce;
    border-bottom: solid 3px #3867ac;
    box-shadow: inset 0 0 0 1px #bbcfeb; }
    
.facebook:active {
    background: #638ec8;
    background: -webkit-gradient(linear, 0 0, 0 bottom, from(#638ec8), to(#99b6df));
    background: -moz-linear-gradient(#638ec8, #99b6df);
    background: linear-gradient(#638ec8, #99b6df);
    border: solid 1px #6d94ce;
    box-shadow: inset 0 10px 15px 0 #4176c4; 
}

.rss {
    background: #f6c696;
    background: -webkit-gradient(linear, 0 0, 0 bottom, from(#f6c696), to(#e9893d));
    background: -moz-linear-gradient(#f6c696, #e9893d);
    background: linear-gradient(#f6c696, #e9893d);
    border: solid 1px #a1681b;
    border-bottom: solid 3px #a1671d;
    box-shadow: inset 0 0 0 1px #f1bb8f;
    color: #fff;
    text-shadow: 0 1px 0 #a1671d; }
    
.rss:hover {
    background: #e9893d;
    background: -webkit-gradient(linear, 0 0, 0 bottom, from(#e9893d), to(#f6c696));
    background: -moz-linear-gradient(#e9893d, #f6c696);
    background: linear-gradient(#e9893d, #f6c696);
    border: solid 1px #a1681b;
    border-bottom: solid 3px #a1671d;
    box-shadow: inset 0 0 0 1px #f1bb8f; }
    
.rss:active {
    background: #e9893d;
    background: -webkit-gradient(linear, 0 0, 0 bottom, from(#e9893d), to(#f6c696));
    background: -moz-linear-gradient(#e9893d, #f6c696);
    background: linear-gradient(#e9893d, #f6c696);
    border: solid 1px #a1681b;
    box-shadow: inset 0 10px 15px 0 #a1671d;
}

.dribbble {
    background: #f1a4c1;
    background: -webkit-gradient(linear, 0 0, 0 bottom, from(#f1a4c1), to(#e675a0));
    background: -moz-linear-gradient(#f1a4c1, #e675a0);
    background: linear-gradient(#f1a4c1, #e675a0);
    border: solid 1px #e98eb0;
    border-bottom: solid 3px #cc4a79;
    box-shadow: inset 0 0 0 1px #f6c2d7;
    color: #fff;
    text-shadow: 0 1px 0 #d64570; }
    
.dribbble:hover {
    background: #e675a0;
    background: -webkit-gradient(linear, 0 0, 0 bottom, from(#e675a0), to(#f1a4c1));
    background: -moz-linear-gradient(#e675a0, #f1a4c1);
    background: linear-gradient(#e675a0, #f1a4c1);
    border: solid 1px #e98eb0;
    border-bottom: solid 3px #cc4a79;
    box-shadow: inset 0 0 0 1px #f6c2d7; }
    
.dribbble:active {
    background: #e675a0;
    background: -webkit-gradient(linear, 0 0, 0 bottom, from(#e675a0), to(#f1a4c1));
    background: -moz-linear-gradient(#e675a0, #f1a4c1);
    background: linear-gradient(#e675a0, #f1a4c1);
    border: solid 1px #e98eb0;
    box-shadow: inset 0 10px 15px 0 #e05285; }

.twitter {
  background: #9fd6fa;
  background: -webkit-gradient(
    linear,
    0 0,
    0 bottom,
    from(#9fd6fa),
    to(#6bb9f7)
  );
  background: -moz-linear-gradient(#9fd6fa, #6bb9f7);
  background: linear-gradient(#9fd6fa, #6bb9f7);
  border: solid 1px #72bdf4;
  border-bottom: solid 3px #4a9de1;
  box-shadow: inset 0 0 0 1px #bfe4fc;
  color: #fff;
  text-shadow: 0 1px 0 #4598f3;
}

.twitter:hover {
  background: #6bb9f7;
  background: -webkit-gradient(
    linear,
    0 0,
    0 bottom,
    from(#6bb9f7),
    to(#9fd6fa)
  );
  background: -moz-linear-gradient(#6bb9f7, #9fd6fa);
  background: linear-gradient(#6bb9f7, #9fd6fa);
  border: solid 1px #72bdf4;
  border-bottom: solid 3px #4a9de1;
  box-shadow: inset 0 0 0 1px #bfe4fc;
}

.twitter:active {
  background: #6bb9f7;
  background: -webkit-gradient(
    linear,
    0 0,
    0 bottom,
    from(#6bb9f7),
    to(#9fd6fa)
  );
  background: -moz-linear-gradient(#6bb9f7, #9fd6fa);
  background: linear-gradient(#6bb9f7, #9fd6fa);
  border: solid 1px #72bdf4;
  box-shadow: inset 0 10px 15px 0 #50aaf3;
}

.twitter p {
  font-family: CookieRun-Bold;
  display: table-cell;
  vertical-align: middle;
  font-size: 3vw;
  color: white
}

#MY_PROGRESS :first-child {
  opacity: 0.9 !important;
  background-color: white !important
}

</style>
