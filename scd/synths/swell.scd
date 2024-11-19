SynthDef.new(\swell,
{|amp=1, sus=1, pan=0, freq=440, fmod=0, rate=1, blur=1, level=0.8|
var osc, env;
sus = sus * blur;
freq = [freq, freq+fmod];
amp=(amp / 4);
freq=(freq + [0, 1]);
freq=(freq * [1, 0.5]);
osc=VarSaw.ar(freq, width: SinOsc.ar((rate / ((2 * sus) / 1.25)), add: 0.5, mul: [0.5, 0.5]), mul: [1, 0.5]);
env=EnvGen.ar(Env.perc(attackTime: 0.01,releaseTime: sus,level: amp,curve: 0), doneAction: 14);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
Out.ar(0, osc)}).add;
