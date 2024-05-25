

// 监听鼠标移动事件，更新自定义光标的位置
document.addEventListener('mousemove', function (e) {
    var cursor = document.querySelector('.cursor');
    cursor.style.left = e.pageX + 'px';
    cursor.style.top = e.pageY + 'px';
});

// 获取画布并设置上下文
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
// 设置画布大小的函数
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

// 初始化画布大小
resizeCanvas();

// 监听窗口变化事件，并调整画布大小
window.addEventListener('resize', resizeCanvas);

const particlesArray = [];
const numberOfParticles = 1; // 每次移动生成的粒子数量

const mouse = {
    x: null,
    y: null
}

// 监听鼠标移动事件，更新鼠标位置并生成粒子
window.addEventListener('mousemove', function (event) {
    mouse.x = event.x;
    mouse.y = event.y;
    for (let i = 0; i < numberOfParticles; i++) {
        particlesArray.push(new Particle());
    }
});
// 粒子类
class Particle {
    constructor() {
        this.x = mouse.x;
        this.y = mouse.y;
        this.size = Math.random() * 2 + 1; // 粒子的随机小尺寸
        this.speedX = Math.random() * 1 - 0.5; // 粒子的水平速度
        this.speedY = Math.random() * 1 - 0.5; // 粒子的垂直速度
        this.color = `#6DA7FD`;
        this.opacity = 1; // 初始透明度
        this.life = 100; // 粒子的生命时长
    }
    update() {
        this.x += this.speedX; // 更新粒子水平位置
        this.y += this.speedY; // 更新粒子垂直位置
        this.life -= 2; // 递减生命时长
    }
    draw() {
        ctx.fillStyle = this.color; // 设置粒子颜色
        ctx.globalAlpha = this.life / 100; // 根据剩余生命时长设置透明度
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2); // 绘制粒子
        ctx.fill();
        ctx.globalAlpha = 1; // 重置透明度
    }
}

// 处理粒子数组，更新和绘制每个粒子
function handleParticles() {
    for (let i = particlesArray.length - 1; i >= 0; i--) {
        particlesArray[i].update(); // 更新粒子位置和生命时长
        particlesArray[i].draw(); // 绘制粒子
        if (particlesArray[i].life <= 0) {
            particlesArray.splice(i, 1); // 生命时长耗尽时删除粒子
        }
    }
}
// 动画循环
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // 清除画布
    handleParticles(); // 处理和绘制粒子
    requestAnimationFrame(animate); // 递归调用animate，实现动画
}

// 开始动画
animate();
