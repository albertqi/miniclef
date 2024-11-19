SynthDef.new(\arpy,
{|amp=1, sus=1, pan=0, freq=440, fmod=0, blur=1|
var osc, env;
sus = sus * blur;
freq = [freq, freq+fmod];
freq=(freq / 2);
amp=(amp * 2);
freq=(freq + [0, 0.5]);
osc=LPF.ar(Impulse.ar(freq), 3000);
env=EnvGen.ar(Env.perc(attackTime: 0.01,releaseTime: (sus * 0.25),level: amp,curve: 0), doneAction: 14);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
Out.ar(0, osc)}).add;
