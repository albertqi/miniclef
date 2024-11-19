SynthDef.new(\sitar,
{|amp=1, sus=1, pan=0, freq=440, fmod=0, blur=1|
var osc, env;
sus = sus * blur;
freq = [freq, freq+fmod];
amp=(amp * 0.75);
sus=(sus * 4);
osc=LFNoise0.ar([8400, 8500], amp);
osc=(osc * XLine.ar(1, 1e-06, (sus * 0.1)));
freq=((265 / (freq * [0.666, 0.669])) * 0.005);
osc=CombL.ar(osc, delaytime: freq, maxdelaytime: 2);
env=EnvGen.ar(Env(times: [sus],levels: [(amp * 1), (amp * 1)],curve: 'step'), doneAction: 14);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
Out.ar(0, osc)}).add;